from django.contrib import admin
from .models import Location

from django.db import connection

# Register your models here.

class LocationAdmin(admin.ModelAdmin):
	# form = LocationForm
	list_display = ('__str__', 'type', 'address')

admin.site.register(Location, LocationAdmin)