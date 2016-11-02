#Customer Admin
from django.contrib import admin


from .models import Customer

from django.db import connection
# Register your models here.

# class CustomerAdmin(admin.ModelAdmin):
# 	
admin.site.register(Customer)