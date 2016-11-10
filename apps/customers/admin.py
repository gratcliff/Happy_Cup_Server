#Customer Admin
from django.contrib import admin


from .models import Customer

from django.db import connection
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):

	def has_add_permission (self, request):
		return False

# 	
admin.site.register(Customer, CustomerAdmin)