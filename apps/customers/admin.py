#Customer Admin
from django.contrib import admin


from .models import Customer, ShippingAddress, WholesalePrice

from django.db import connection
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'registered', 'user')
	list_filter = ('registered',)
	search_fields = ['user__email', 'id', 'user__first_name', 'user__last_name', 'name', 'email']


	def get_readonly_fields(self, request, obj):
		if obj is None:
			return ['id', 'stripe_id', 'name', 'email', 'phone_number', 'address', 'address2', 'city', 'state', 'zipcode']
		return ['id', 'registered', 'stripe_id', 'user', 'name', 'email', 'phone_number', 'address', 'address2', 'city', 'state', 'zipcode']

	def has_add_permission (self, request):
		return False



	
admin.site.register(Customer, CustomerAdmin)
admin.site.register(WholesalePrice)
admin.site.register(ShippingAddress)