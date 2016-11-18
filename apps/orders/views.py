from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.utils import timezone

from ..customers.models import Customer, ShippingAddress
from ..customers.forms import CustomerShippingForm

from ..products.models import Coupon

from .models import CustomerOrder


import json
import os
import stripe
import time




# Create your views here.

class VerifyCouponCode(View):

	def post(self, request):
		code = request.body
		shoppingCart = request.session.get('shoppingCart')
		try:
			coupon = Coupon.objects.get(code__iexact=code, expiration_date__gt=timezone.now())

			if coupon.is_valid_coupon():

				shoppingCart['coupon']['code'] = coupon.code
				shoppingCart['coupon']['valid'] = True
				shoppingCart['coupon']['discount'] = coupon.discount
				request.session['shoppingCart'] = shoppingCart

				return JsonResponse(request.session['shoppingCart']['coupon'])

		except Exception as e:
			print e.args


		
		return JsonResponse({'error': 'Invalid coupon code'})


class CheckShippingAddress(View):

	def post(self, request):

		loadJson = json.loads(request.body)
		form = CustomerShippingForm(loadJson)

		if form.is_valid():
			shoppingCart = request.session["shoppingCart"]

			shoppingCart["shipping"] = loadJson

			try:
				shoppingCart['shipping']['address'] = "%s %s" % (form.cleaned_data['verify_address']['number'], form.cleaned_data['verify_address']['street'])
				shoppingCart['shipping']['city'] = form.cleaned_data['verify_address']['city']
				shoppingCart['shipping']['state'] = form.cleaned_data['verify_address']['state']
				shoppingCart['shipping']['zipcode'] = form.cleaned_data['verify_address']['zipcode']

				if shoppingCart['shipping'].get('saveShipping') is True:
					user_id = shoppingCart['shipping'].get('user_id')
					customer_id = shoppingCart['shipping'].get('customer_id')

					if user_id == request.user.id:
						if not customer_id:

							customer = Customer()
							customer.user = request.user
							customer.migrate_data(shoppingCart)
							customer.save()

							shippingAddress = ShippingAddress()
							shippingAddress.migrate_data(shoppingCart)
							shippingAddress.customer = customer
							shippingAddress.save()
							shoppingCart['shipping']['customer_id'] = customer.id
						else:

							customer = Customer.objects.prefetch_related('shippingaddress_set').get(id=customer_id)
							customer.migrate_data(shoppingCart)
							customer.save()

							try:
								shippingAddress = ShippingAddress()
								shippingAddress.migrate_data(shoppingCart)
								shippingAddress.customer = customer
								shippingAddress.save()
							except Exception as e:
								print e.args
					else:
						logout(request)
						return JsonResponse({'status': False, 'security': 'You have been logged out for security reasons.  Please try again.'})

			except Exception as e:
				if form.cleaned_data.get('api_arror'):
					shoppingCart['api_error'] = form.cleaned_data['api_error']
				else:
					print e.args


			shoppingCart['checkoutStatus']['payment'] = True
			request.session["shoppingCart"] = shoppingCart

			return JsonResponse({"status": True, 'shoppingCart': request.session["shoppingCart"]})

		else:
			return JsonResponse({"status": False, "errors": form.errors.as_json()})


class ProcessPayment(View):

	def post(self, request):
		post_data = json.loads(request.body)
		shoppingCart = request.session.get('shoppingCart')
		if len(shoppingCart['wholeSaleCoffee']):
			shoppingCart['coffee'].extend(shoppingCart['wholeSaleCoffee'])
		amount = int(shoppingCart['totalPrice']*100)
		
		source = post_data.get('token')
		receipt_email = post_data.get('email')
		phone_number = post_data.get('phone_number')
		
		order = None
		customer = None
		coupon = None
		charge = None
		user = request.user

		try:
			if shoppingCart['coupon'].get('code'):
				coupon = Coupon.objects.get(code__iexact=shoppingCart['coupon']['code'])
				if coupon.is_valid_coupon():
					shoppingCart['totalPrice'] = float("{0:.2f}".format(shoppingCart['totalPrice'] * (1-(coupon.discount/100.0)),))
				else:
					return JsonResponse({'coupon_error': 'Your order could not be completed. The coupon code used is no longer valid and has been removed. Please try again.'})
		except Exception as e:
			print e.args
			return JsonResponse({'coupon_error': 'Your order could not be completed. The coupon code used is not valid and has been removed. Please try again.'})

		try:
			amount = int(shoppingCart['totalPrice']*100)
			description = '%s items' % (str(shoppingCart['totalItems']),)

			if user.is_authenticated:

				charge = stripe_charge(amount, source, description, receipt_email)
				customer = Customer.objects.get(user=user)
				shippingAddress = ShippingAddress()
				shippingAddress.migrate_data(shoppingCart)
				order = CustomerOrder()
				order.migrate_data(shoppingCart, customer, coupon, shippingAddress.shipping_address)
				order.charge_id = charge['id']
				order.save()

			else:

				charge = stripe_charge(amount, source, description, receipt_email)
				customer = Customer()
				customer.migrate_data(shoppingCart)
				customer.save()

				order = CustomerOrder()
				order.migrate_data(shoppingCart, customer, coupon, customer.shipping_address)
				order.charge_id = charge['id']
				order.save()

			charge_metadata = {
				'HC_order_id': order.id,
				'shipping_address': order.parse_shipping_address(True),
				'billing_phone' : phone_number
			}

			coffee_metadata = order.parse_coffee(True)
			merch_metadata = order.parse_merchandise(True)

			if len(coffee_metadata) + len(merch_metadata) < 18:

				for idx in range(len(coffee_metadata)):

					charge_metadata['coffee0'+str(idx+1)] = coffee_metadata[idx] if len(coffee_metadata[idx]) < 500 else coffee_metadata[idx][:499]

				for idx in range(len(merch_metadata)):

					charge_metadata['merchandise0'+str(idx+1)] = merch_metadata[idx] if len(merch_metadata[idx]) < 500 else merch_metadata[idx][:499]
			else:

				charge_metadata['many_items'] = 'Too many items were ordered and could not be added to metadata'

			update_charge = stripe.Charge.retrieve(charge['id'])
			update_charge.shipping = order.parse_shipping_address(False, True)
			del update_charge.shipping['email']
			update_charge.metadata = charge_metadata
			update_charge.save()			
			
			del request.session['shoppingCart']
		except stripe.error.CardError as e:
			return JsonResponse(e.json_body)
		except Exception as e:
			if charge['status'] == 'succeeded':

				try:
					time.sleep(1.0)
					update_charge = stripe.Charge.retrieve(charge['id'])
					update_charge.shipping = order.parse_shipping_address(False, True)
					del update_charge.shipping['email']
					update_charge.metadata = {
						'HC_order_id': order.id,
						'shipping_address': order.parse_shipping_address(True),
						'billing_phone' : phone_number,
						'metadata_error' : str(e)
					}
					update_charge.save()
					del request.session['shoppingCart']
				except Exception as e:
					print e

				return JsonResponse({'status':True, 'order_id':order.id, 'customer_id': customer.id})
	

			return JsonResponse({'error': {'message':'Your online order could not be processed at this time.  Please try again later.'}})


		return JsonResponse({'status':True, 'order_id':order.id, 'customer_id': customer.id})

class SendEmailConfirmation(View):

	def post(self, request):
		try:
			data = json.loads(request.body)
			order_id = data.get('order_id')
			cust_id = data.get('customer_id')
			order = CustomerOrder.objects.select_related('customer', 'coupon', 'customer__wholesale_price').get(id=int(order_id), customer_id=int(cust_id))
			charge = stripe.Charge.retrieve(order.charge_id)

			order.send_email_confirmation(charge)
		except Exception as e:
			print e.args

		return JsonResponse({'status': True})



class ProvideInvoice(View):

	def post(self, request):
		try:
			data = json.loads(request.body)
			order_id = data.get('order_id')
			cust_id = data.get('customer_id')
			order = CustomerOrder.objects.select_related('customer', 'coupon', 'customer__wholesale_price').get(id=int(order_id), customer_id=int(cust_id))
			charge = stripe.Charge.retrieve(order.charge_id)
			order_json = order.serialize_model()

			response = {'charge':{'shipping': charge['shipping'], 'source': charge['source']}, 'order':order_json}
			response['charge']['source']['phone_number'] = charge['metadata'].get('billing_phone')
			response['charge']['source']['email'] = charge.get('receipt_email')

			return JsonResponse(response)

		except Exception as e:
			print e
			return JsonResponse({'status': False})


def stripe_charge(amount, source, description, receipt_email):
	charge = stripe.Charge.create(
					amount = amount,
					currency = 'usd',
					source = source,
					description = description,
					receipt_email = receipt_email
				)	
	return charge		





