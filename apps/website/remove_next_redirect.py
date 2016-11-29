from django.conf import settings
from django.http import HttpResponseRedirect

class RemoveNextMiddleware(object):

		def __init__(self, get_response):
			self.get_response = get_response

		def __call__(self, request):
			response = self.get_response(request)
			if request.path == settings.LOGIN_URL and 'next' in request.GET:
				return HttpResponseRedirect(settings.LOGIN_URL)
			if request.path == '/admin/login/' and 'next' in request.GET:
				return HttpResponseRedirect(settings.LOGIN_URL)
			return response
