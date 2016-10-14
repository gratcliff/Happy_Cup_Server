from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
class Index(View):

	def get(self, request):

		if 'authorizedUser' not in request.session:
			request.session['authorizedUser'] = False

		return render(request, 'website/index.html')

	
	def post(self, request):

		if request.body == 'or97232':
			print 'request.body'
			request.session['authorizedUser'] = True
			return JsonResponse({'status': True})
		else:
			print False
			request.session['authorizedUser'] = False
			return JsonResponse({'status': False})
