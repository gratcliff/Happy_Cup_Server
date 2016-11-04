from django.shortcuts import render

from django.http import JsonResponse
from ..customers.forms import CustomerShippingForm

import json

# Create your views here.

def checkShippingAddress(request):

	loadJson = json.loads(request.body)
	form = CustomerShippingForm(loadJson["shippingInfo"])

	if form.is_valid():
		shoppingCart = request.session["shoppingCart"]


		shoppingCart["billing"] = loadJson["billingInfo"]

		shoppingCart["shipping"] = loadJson["shippingInfo"]

		shoppingCart['shipping']['address'] = "%s %s" % (form.cleaned_data['verify_address'][0], form.cleaned_data['verify_address'][1])
		shoppingCart['shipping']['city'] = form.cleaned_data['verify_address'][2]
		shoppingCart['shipping']['state'] = form.cleaned_data['verify_address'][3]
		shoppingCart['shipping']['zipcode'] = form.cleaned_data['verify_address'][4]

		request.session["shoppingCart"] = shoppingCart
		

		return JsonResponse({"status": True, 'shoppingCart': request.session["shoppingCart"]})
	else:
		return JsonResponse({"status": False, "errors": form.errors.as_json()})

