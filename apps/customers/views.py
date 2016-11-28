from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User 
from .forms import UserRegisterForm, UserEditForm

from django.contrib.auth import authenticate, login, logout

from ..website.serialize import JsonSerializer
from .models import ShippingAddress, Customer


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
		print "user is being edited"
		form = UserEditForm(json.loads(request.body))

		if form.is_valid():
			prev_username = json.loads(request.body)["prev_username"]
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			user = User.objects.get(username=prev_username)
			user.username = username
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.save()

			# Customer.objects.filter(email=email).update(username=username,first_name=first_name,last_name=last_name, email=email)
			user_json = serialize.serialize_user(user)

		else:
			return JsonResponse({'status': False, 'errors': form.errors.as_json()})


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



def logout_user(request):
	logout(request)
	request.session['authorizedUser'] = True
	return JsonResponse({'status':True})

		



	

