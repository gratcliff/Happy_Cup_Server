from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def registerUser(request):
	return JsonResponse({'status': True});

