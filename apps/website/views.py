from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import connection


import serialize
from querysets import QuerySet
from contentprovider import ContentProvider
from shopping_cart import ShoppingCart, empty_all_carts


import json
import os

# Create your views here.


class Index(View):

	@method_decorator(ensure_csrf_cookie)
	def get(self, request):

		self.context = {

			'MAPSAPI_KEY' : os.environ.get('MAPSAPI_KEY','')

		}

		return render(request, 'website/index.html', self.context)


class ProvideContent(View):

	content = ContentProvider()

	try:
		content.populate_products()
		content.populate_aboutPage()
		content.populate_locations()
		content.populate_news()

	except Exception as e:
		print e

	

	def get(self,request):

		self.content.query_set = QuerySet()
		
		self.content.expired_promotion_check()
		self.content.refresh_geocodes()			

		if serialize.db_modified:
			print 'refreshing data'
			self.content.populate_products()
			self.content.populate_aboutPage()
			self.content.populate_locations()
			self.content.populate_news()
			if serialize.db_price_change:
				# if database data that could alter product pricing is modified, all user shopping carts get emptied
				serialize.db_price_change = False
				empty_all_carts()

		self.context = {
			'home' : {

				'products' : {
					'featured' : self.content.featured_products,
					'coffee' : self.content.coffee_json,
					'wholeSaleCoffee' : self.content.wholeSaleCoffee_json,
					'merchandise' : self.content.merchandise_json,
					'subscriptions' : self.content.subscription_json
				},
			},
			'about' : {
				'fullWidthSection' : self.content.about_fullWidthSection,
				'staffMemberEntry' : self.content.about_staffMemberEntry
			},
			'locations': self.content.locations,
			'blogPosts': self.content.blogPosts,
			'stripe_public_key' : os.environ.get('STRIPE_PUB_TEST')
		}

		print len(connection.queries)

		return JsonResponse(self.context, safe=False)



class SyncShoppingCart(View):

	def get(self, request):

		# request.session.clear()

		cart_exists = request.session.get('shoppingCart', None)
		if not cart_exists:
			shoppingCart = ShoppingCart()
			request.session['shoppingCart'] = shoppingCart.to_dictionary() 

		return JsonResponse(request.session['shoppingCart'])

	def post(self, request):
		cart = json.loads(request.body)
		print cart

		cart['unsavedChanges'] = False
		cart['checkoutStatus']['review'] = False

		if cart['totalItems'] == 0:
			shoppingCart = ShoppingCart()
			request.session['shoppingCart'] = shoppingCart.to_dictionary()
			return JsonResponse({'shoppingCart': request.session['shoppingCart']}) 
		else:
			request.session['shoppingCart'] = cart

		return JsonResponse({'status': True})




