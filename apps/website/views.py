from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import connection




import serialize
from querysets import QuerySet
from shopping_cart import ShoppingCart


import json

# Create your views here.


class Index(View):

	@method_decorator(ensure_csrf_cookie)
	def get(self, request):

		return render(request, 'website/index.html')


class ProvideContent(View):

	query_set = QuerySet()
	json_serializer = serialize.JsonSerializer()
	coffee_json = json_serializer.serialize_coffee(query_set.coffee)
	merchandise_json = json_serializer.serialize_merch(query_set.merchandise)
	variety_pack_json = json_serializer.serialize_variety(query_set.variety_pack)

	# concatenate merchadise and variety pack lists
	merchandise_json.extend(variety_pack_json)


	def get(self,request):
		if serialize.db_modified:
			self.query_set = QuerySet() # redefine to wipe cached data
			self.coffee_json = self.json_serializer.serialize_coffee(self.query_set.coffee)
			self.merchandise_json = json_serializer.serialize_merch(self.query_set.merchandise)
			self.variety_pack_json = json_serializer.serialize_variety(self.query_set.variety_pack)
			
			# concatenate merchadise and variety pack lists
			self.merchandise_json.extend(self.variety_pack_json)

		context = {
			'home' : {

				'products' : {
					'coffee' : self.coffee_json,
					'merchandise' : self.merchandise_json,
				},
			},
		}

		return JsonResponse(context, safe=False)



class SyncShoppingCart(View):

	def get(self, request):

		# request.session.clear()

		if 'shoppingCart' not in request.session:
			shoppingCart = ShoppingCart()
			request.session['shoppingCart'] = shoppingCart.to_dictionary()
			return JsonResponse({'new': True})


		return JsonResponse(request.session['shoppingCart'])

	def post(self, request):
		cart = json.loads(request.body)

		request.session['shoppingCart'] = cart

		return JsonResponse({'status': True})




