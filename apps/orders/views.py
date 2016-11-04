from django.shortcuts import render

from django.http import JsonResponse
from ..customers.forms import CustomerShippingForm

import json

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

