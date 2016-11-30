from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User 
from .forms import UserRegisterForm, UserEditForm

from django.contrib.auth import authenticate, login, logout

from ..website.serialize import JsonSerializer
from ..orders.models import CustomerOrder, SubscriptionOrder

from .models import ShippingAddress, Customer

from django.db import connection



import json

serialize = JsonSerializer()

# Create your views here.

class RegisterUser(View):

	# print request.body
	def post(self, request):

		form = UserRegisterForm(json.loads(request.body))

		if form.is_valid():
			user = form.save()
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, email=email, password=password)
			if user is not None:
				login(request, user)
				Customer.objects.create(user=user, email=email, name="%s %s"%(user.first_name, user.last_name), registered=True)
				user_json = serialize.serialize_user(user)

				return JsonResponse({'status': True, 'user':user_json});
			else:
				return JsonResponse({'status' : False, 'errors': form.errors.as_json()})
		else:
			return JsonResponse({'status': False, 'errors': form.errors.as_json()})

class EditUser(View):

	def post(self, request):

		data = json.loads(request.body)

		# switch methods if deleting saved address
		if data.get('address'):
			self.delete_address(data['address'])
			user_json = serialize.serialize_user(request.user)
			return JsonResponse({'status': True, 'user':user_json});

		form = UserEditForm(data, instance=request.user)

		if form.is_valid():
			user = form.save()

			user_json = serialize.serialize_user(user)
			return JsonResponse({'status': True, 'user':user_json}); 

		else:
			return JsonResponse({'status': False, 'errors': form.errors.as_json()})

	def delete_address(self, id):
		
		address = ShippingAddress.objects.get(id=int(id))
		address.delete()


class LoginUser(View):

	def post(self, request):
		body = json.loads(request.body)
		username = body.get('email_username')
		password = body.get('password')
		if '@' in username:
			try:

				auth = User.objects.get(email=username)
				user = authenticate(username=auth.username, password=password)

				if user is not None:

					login(request, user)
					user_json = serialize.serialize_user(user)
					return JsonResponse({'status': True, 'user':user_json});

				else:
					return JsonResponse({'status': False})

			except Exception as e:
				user = authenticate(username=username, password=password)
				if user is not None:

					login(request, user)
					user_json = serialize.serialize_user(user)
					return JsonResponse({'status': True, 'user':user_json});

				else:
					return JsonResponse({'status': False})

		else:
			user = authenticate(username=username, password=password)
			if user is not None:

				login(request, user)
				user_json = serialize.serialize_user(user)
				return JsonResponse({'status': True, 'user':user_json});

			else:
				return JsonResponse({'status': False})


		return JsonResponse({'status': False})

		


class GetCurrentUser(View):

	def get(self, request):

		if request.user.is_authenticated:
			
			user_json = serialize.serialize_user(request.user)
			return JsonResponse({'status': True, 'user':user_json});

		return JsonResponse({'status': False})


class GetOrderHistory(View):

	def get(self, request):

		customer = Customer.objects.select_related('wholesale_price').prefetch_related('customerorder_set', 'subscriptionorder_set', 'customerorder_set__coupon','subscriptionorder_set__subscription').get(user=request.user)

		orders = customer.customerorder_set.all()
		subscriptions = customer.subscriptionorder_set.all()

		orders_json = [order.serialize_model(True) for order in orders]
		subscription_json = [sub.serialize_model() for sub in subscriptions]

		return JsonResponse({'orders':orders_json, 'subscriptions':subscription_json})
		

def logout_user(request):
	logout(request)
	request.session['authorizedUser'] = True
	return JsonResponse({'status':True})

		



	

