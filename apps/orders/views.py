from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.utils.html import format_html

from ..customers.models import Customer
from ..customers.forms import CustomerShippingForm

from .models import CustomerOrder


import json
import os
import stripe
import time



# Create your views here.

def checkShippingAddress(request):

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
		except Exception as e:
			shoppingCart['api_error'] = form.cleaned_data['api_error']


		shoppingCart['checkoutStatus']['payment'] = True
		request.session["shoppingCart"] = shoppingCart
		

		return JsonResponse({"status": True, 'shoppingCart': request.session["shoppingCart"]})

	else:
		return JsonResponse({"status": False, "errors": form.errors.as_json()})


class ProcessPayment(View):

	stripe.api_key = os.environ.get('STRIPE_SECRET_TEST')

	def post(self, request):
		token = json.loads(request.body).get('token')
		email = json.loads(request.body).get('email')
		shoppingCart = request.session.get('shoppingCart')
		order = None
		customer = None

		try:
			charge = stripe.Charge.create(
					amount = int(shoppingCart['totalPrice']*100),
					currency = 'usd',
					source = token,
					description = '%s items' % (str(shoppingCart['totalItems']),),
					receipt_email = email
				)

			customer = Customer()
			customer.migrate_data(shoppingCart)
			customer.save()

			order = CustomerOrder()
			order.migrate_data(shoppingCart, customer)
			order.charge_id = charge['id']
			order.save()

			charge_metadata = {
				'HC_order_id': order.id,
				'shipping_address': customer.shipping_address(True),
				'num_items': shoppingCart['totalItems'],
			}

			coffee_metadata = order.parse_coffee(True)
			merch_metadata = order.parse_merchandise(True)

			if len(coffee_metadata) + len(merch_metadata) > 18:
				for idx in range(len(coffee_metadata)):
					charge_metadata['coffee0'+str(idx+1)] = coffee_metadata[idx] if len(coffee_metadata[idx]) < 500 else coffee_metadata[idx][:499]

				for idx in range(len(merch_metadata)):
					charge_metadata['merchandise0'+str(idx+1)] = merch_metadata[idx] if len(merch_metadata[idx]) < 500 else merch_metadata[idx][:499]
			else:
				charge_metadata['many_items'] = 'Too many items were ordered and could not be added to metadata'
			
			update_charge = stripe.Charge.retrieve(charge['id'])
			update_charge.shipping = customer.migrate_data(shoppingCart, True)
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
					update_charge.shipping = customer.migrate_data(shoppingCart, True)
					update_charge.metadata = {
						'HC_order_id': order.id,
						'shipping_address': customer.shipping_address(True),
						'num_items': shoppingCart['totalItems'],
						'metadata_error' : str(e)
					}
					update_charge.save()
					del request.session['shoppingCart']
				except Exception as e:
					print e

				return JsonResponse({'status':True, 'order_id':order.id})
	

			return JsonResponse({'error': {'message':'Your online order could not be processed at this time.  Please try again later.'}})




		return JsonResponse({'status':True, 'order_id':order.id})







class ProvideInvoice(View):

	def get(self, request):
		print request.body
		try:
			order = CustomerOrder.objects.select_related('customer', 'coupon', 'customer__discount_rate').get(id=int(request.body))
			charge = stripe.Charge.retrieve(order.charge_id)

			order_json = order.serialize_model
			
			return JsonResponse({'charge':charge, 'order':order_json})

		except Exception as e:
			return JsonResponse({'status': False})




