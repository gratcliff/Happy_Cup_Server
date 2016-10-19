from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection




import serialize
from querysets import QuerySet


import json

# Create your views here.
class Index(View):

	def get(self, request):

		return render(request, 'website/index.html')


class ProvideContent(View):

	query_set = QuerySet()
	json_serializer = serialize.JsonSerializer()
	coffee_json = json_serializer.serialize_coffee(query_set.coffee)

	def get(self,request):
		if serialize.db_modified:
			self.query_set = QuerySet() # redefine to wipe cached data
			self.coffee_json = self.json_serializer.serialize_coffee(self.query_set.coffee)

		return JsonResponse(self.coffee_json, safe=False)