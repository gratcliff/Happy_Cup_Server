from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.utils import timezone

from ..customers.models import Customer, ShippingAddress
from ..customers.forms import CustomerShippingForm

from ..products.models import Coupon, Subscription

from .models import CustomerOrder, SubscriptionOrder, ShippingFee

from ..website.serialize import JsonSerializer


import json
import os
import stripe
import time
import math

serialize = JsonSerializer()


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
			shoppingCart['shippingFee'] = 0
			saveShipping = False

			try:
				shoppingCart['shipping']['address'] = "%s %s" % (form.cleaned_data['verify_address']['number'], form.cleaned_data['verify_address']['street'])
				shoppingCart['shipping']['city'] = form.cleaned_data['verify_address']['city']
				shoppingCart['shipping']['state'] = form.cleaned_data['verify_address']['state']
				shoppingCart['shipping']['zipcode'] = form.cleaned_data['verify_address']['zipcode']

				if shoppingCart['shipping'].get('saveShipping') is True:
					user_id = shoppingCart['shipping'].get('user_id')
					customer_id = shoppingCart['shipping'].get('customer_id')
					saveShipping = True

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
								saveShipping = False
								print e.args
					else:
						logout(request)
						return JsonResponse({'status': False, 'security': 'You have been logged out for security reasons.  Please try again.'})

			except Exception as e:
				if form.cleaned_data.get('api_arror'):
					shoppingCart['api_error'] = form.cleaned_data['api_error']
				else:
					print e.args

			if len(shoppingCart.get('subscriptions')) > 0:

				for sub in shoppingCart.get('subscriptions'):
					weight = math.ceil(sub['ship_wt'])
					shipping_fee = ShippingFee.objects.filter(min_weight__lte=int(weight), max_weight__gte=int(weight))[0].price
					shipping_fee = round((shipping_fee*100 / sub['qty'])) / 100
					sub['shipping_fee'] = shipping_fee
					
					shoppingCart['shippingFee'] += shipping_fee * sub['qty']
			else :

				weight = math.ceil(shoppingCart['totalWeight'])
				shipping_fee = ShippingFee.objects.filter(min_weight__lte=int(weight), max_weight__gte=int(weight))
				shoppingCart['shippingFee'] = shipping_fee[0].price
			
			shoppingCart['checkoutStatus']['payment'] = True

			if saveShipping:
				user_json = serialize.serialize_user(User.objects.get(id=request.user.id))
				shoppingCart['user'] = user_json
			else:
				user_json = None

			request.session["shoppingCart"] = shoppingCart

			return JsonResponse({"status": True, 'shoppingCart': request.session["shoppingCart"], 'user':user_json})

		else:
			return JsonResponse({"status": False, "errors": form.errors.as_json()})


class ProcessPayment(View):

	def post(self, request):
		post_data = json.loads(request.body)
		shoppingCart = request.session.get('shoppingCart')

		shoppingCart['subTotalPrice'] = shoppingCart['totalPrice']
		
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
					shoppingCart['totalPrice'] *= 100
					shoppingCart['totalPrice'] = round(shoppingCart['totalPrice'] * (1-(coupon.discount/100.0))) 
					shoppingCart['totalPrice'] = int(shoppingCart['totalPrice']) / 100.0
				else:
					return JsonResponse({'coupon_error': 'Your order could not be completed. The coupon code used is no longer valid and has been removed. Please try again.'})
		except Exception as e:
			print e.args
			return JsonResponse({'coupon_error': 'Your order could not be completed. The coupon code used is not valid and has been removed. Please try again.'})

		try:
			amount = int((shoppingCart['totalPrice']+shoppingCart['shippingFee'])*100)
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
			if data.get('subscriptions'):
				orders = SubscriptionOrder.objects.select_related('customer', 'subscription').filter(pk__in=order_id)
				for order in orders:
					order.send_email_confirmation(data['subscriptions'][0])
					if len(orders) > 1:
						time.sleep(0.5)
			else:
				order = CustomerOrder.objects.select_related('customer', 'coupon', 'customer__wholesale_price').filter(pk__in=order_id, customer_id=int(cust_id))[0]
				charge = stripe.Charge.retrieve(order.charge_id)

				order.send_email_confirmation(charge)
		except Exception as e:
			print e.args

		return JsonResponse({'status': True})

class ProcessSubscription(View):

	def post(self, request):
		post_data = json.loads(request.body)
		shoppingCart = request.session.get('shoppingCart')

		shoppingCart['subTotalPrice'] = shoppingCart['totalPrice']
		
		source = post_data.get('token')
		receipt_email = post_data.get('email')
		phone_number = post_data.get('phone_number')
		subscription_list = list(shoppingCart['subscriptions'])
		
		subscription = None
		customer = None
		charge = None
		user = request.user

		plans = []
		for sub in subscription_list:
			query = Subscription.objects.get(id=sub['id'])
			plan = query.create_or_retreive_plan(sub['price'], sub['shipping_fee'])

			if plan.get('api_error'):
				return JsonResponse({'error': {'message':'Your online order could not be processed at this time.  Please try again later.'}})

			plans.append({'plan':plan, 'subscription':sub})
			if len(subscription_list) > 1:
				time.sleep(0.25)


		customer = Customer.objects.get(user=user)
		stripe_customer = customer.create_or_retreive_customer(source, user)

		if stripe_customer.get('api_error'):
			return JsonResponse({'error': {'message':'Your online order could not be processed at this time.  Please try again later.'}})

		subscription_list = []
		for plan in plans:
			plan_id = plan['plan']['id']
			customer_id = stripe_customer['id']
			quantity = plan['subscription']['qty']

			order = SubscriptionOrder()
			stripe_sub = order.create_stripe_subscription(customer_id, plan_id, quantity)

			if stripe_sub.get('api_error'):
				return JsonResponse({'error': {'message':'Your online order could not be processed at this time.  Please try again later.'}})


			shippingAddress = ShippingAddress()
			shippingAddress.migrate_data(shoppingCart)

			order.migrate_data(stripe_sub['id'], plan['subscription'], customer, shippingAddress.shipping_address, shoppingCart['shipping'].get('message',''))
			order.save()

			stripe_sub.metadata = {
				'HC_subscription_id': order.id,
				'shipping_address': order.parse_shipping_address(True),
				'billing_phone' : phone_number,
				'billing_email' : receipt_email,
				'coffee' : order.coffee,
				'grind' : order.grind,
				'size' : order.size,
			}

			stripe_sub.save()
			stripe_customer['sources']['data'][0]['phone_number'] = phone_number
			stripe_customer['sources']['data'][0]['email'] = receipt_email


			subscription_list.append({'order': order.serialize_model(), 'billing': stripe_customer['sources']['data']})

			if len(plans) > 1:
				time.sleep(0.25)

		del request.session['shoppingCart']
		return JsonResponse({'status':True, 'subscription_list':subscription_list, 'customer_id': customer.id})
		



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

class CancelSubscription(View):

	def post(self, request):
		try:
			sub_id = int(request.body)
			sub = SubscriptionOrder.objects.get(id=sub_id)
			stripe_id = sub.stripe_id
			print sub

			subscription = stripe.Subscription.retrieve(stripe_id)

			subscription.delete()

			sub.status = subscription['status']
			sub.save()

			return JsonResponse({'status': True})

		except Exception as e:
			print e.args
			return JsonResponse({'status': False})

def webhooks(request):

	print request.body


def stripe_charge(amount, source, description, receipt_email):
	charge = stripe.Charge.create(
					amount = amount,
					currency = 'usd',
					source = source,
					description = description,
					receipt_email = receipt_email
				)	
	return charge		





