from django.contrib import admin
from .models import Location, StoreType
from .forms import LocationForm

from django.db import connection, models
from django.forms import NumberInput

# Register your models here.

class LocationAdmin(admin.ModelAdmin):
	form = LocationForm
	list_display = ('__str__', 'address')

	formfield_overrides = {
		models.PositiveIntegerField: {'widget': NumberInput()}
	}

admin.site.register(Location, LocationAdmin)
admin.site.register(StoreType)