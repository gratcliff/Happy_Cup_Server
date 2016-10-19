from django.contrib import admin

from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast
from ..products.models import Coffee, FeaturedProduct

# Register your models here.

admin.site.disable_action('delete_selected')

class CoffeeAdmin(admin.ModelAdmin):
	filter_horizontal = ('grinds', 'sizes')


class FeaturedProductAdmin(admin.ModelAdmin):
	filter_horizontal = ('coffees',)


admin.site.register(CoffeeRoast)
admin.site.register(CoffeeGrind)
admin.site.register(CoffeeVolume)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(FeaturedProduct, FeaturedProductAdmin)
