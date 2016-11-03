from django.contrib import admin

from .models import CustomerOrder

from django.db import connection
# Register your models here.

admin.site.register(CustomerOrder)
