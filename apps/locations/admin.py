from django.contrib import admin
from .models import Location, StoreType
from .forms import LocationForm

from django.db import connection

# Register your models here.

class LocationAdmin(admin.ModelAdmin):
	form = LocationForm
	list_display = ('__str__', 'address', 'updated_at')

admin.site.register(Location, LocationAdmin)
admin.site.register(StoreType)