#Customer Admin
from django.contrib import admin


from .models import Customer, ShippingAddress

from django.db import connection
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):

	def get_readonly_fields(self, request, obj):
		return ['id', 'user', 'name', 'email', 'phone_number', 'address', 'address2', 'city', 'state', 'zipcode']

	def has_add_permission (self, request):
		return False

	
admin.site.register(Customer, CustomerAdmin)