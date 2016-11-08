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

			update_charge = stripe.Charge.retrieve(charge['id'])
			update_charge.shipping = customer.migrate_data(shoppingCart, True)
			update_charge.metadata = {'HC_order_id': order.id, 'shipping_address': customer.shipping_address(True), 'num_items': shoppingCart['totalItems']}
			update_charge.save()			
			
			del request.session['shoppingCart']
		except stripe.error.CardError as e:
			return JsonResponse(e.json_body)
		except Exception as e:
			print e
			return JsonResponse({'error': {'message':'Your online order could not be processed at this time.  Please try again later.'}})




		return JsonResponse({'status':True})