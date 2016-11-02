from django.shortcuts import render
from django.http import JsonResponse
from .forms import UserRegisterForm

from django.contrib.auth import authenticate, login, logout

import json

# Create your views here.

def registerUser(request):

	# print request.body

	form = UserRegisterForm(json.loads(request.body))

	if form.is_valid():
		user = form.save()
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password1']
		user = authenticate(username=username, email=email, password=password)
		print user
		if user is not None:
			login(request, user)
			return JsonResponse({'status': True, 'user':user.first_name});
		else:
			return JsonResponse({'status' : False, 'errors': form.errors.as_json()})
	else:
		return JsonResponse({'status': False, 'errors': form.errors.as_json()})



	

