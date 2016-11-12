from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User

from .forms import UserRegisterForm

from django.contrib.auth import authenticate, login, logout

from ..website.serialize import JsonSerializer


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

				user_json = serialize.serialize_user(user)

				return JsonResponse({'status': True, 'user':user_json});
			else:
				return JsonResponse({'status' : False, 'errors': form.errors.as_json()})
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
	return JsonResponse({'status':True})

		



	

