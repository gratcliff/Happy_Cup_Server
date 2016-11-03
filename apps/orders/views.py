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

		request.session["shoppingCart"] = shoppingCart
		print shoppingCart["shipping"]

		return JsonResponse({"status": True, 'shoppingCart': request.session["shoppingCart"]})
	else:
		return JsonResponse({"status": False, "errors": form.errors.as_json()})

