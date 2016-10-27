from django.contrib import admin

from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast, ShirtSize

# Register your models here.

class CoffeeVolumeAdmin(admin.ModelAdmin):
	list_display = ('__str__','base_price')

	

admin.site.register(CoffeeRoast)
admin.site.register(CoffeeGrind)
admin.site.register(ShirtSize)
admin.site.register(CoffeeVolume, CoffeeVolumeAdmin)