from django.contrib import admin

from ..products.forms import VarietyPackForm

from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast, ShirtSize
from ..products.models import Coffee, Subscription, Merchandise, VarietyPack, FeaturedProduct

# Register your models here.

admin.site.disable_action('delete_selected')

class CoffeeAdmin(admin.ModelAdmin):
	filter_horizontal = ('grinds', 'sizes')


class FeaturedProductAdmin(admin.ModelAdmin):
	filter_horizontal = ('coffees',)

class SubscriptionAdmin(admin.ModelAdmin):
	filter_horizontal = ('coffees',)

class MerchandiseAdmin(admin.ModelAdmin):
	filter_horizontal = ('sizes',)

class VarietyPackAdmin(admin.ModelAdmin):
	form = VarietyPackForm
	filter_horizontal = ('coffees','merchandise')


admin.site.register(CoffeeRoast)
admin.site.register(CoffeeGrind)
admin.site.register(CoffeeVolume)
admin.site.register(ShirtSize)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(VarietyPack, VarietyPackAdmin)
admin.site.register(FeaturedProduct, FeaturedProductAdmin)
