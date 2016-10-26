from django.contrib import admin

from ..products.forms import VarietyPackForm

from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast, ShirtSize
from ..products.models import Coffee, Subscription, Merchandise, VarietyPack, ProductPromotion

from django.db import connection

from django.utils import timezone

# Register your models here.

admin.site.disable_action('delete_selected')

class CoffeeAdmin(admin.ModelAdmin):
	filter_horizontal = ('grinds', 'sizes')
	list_display = ('__str__','base_price_smallest','featured')
	list_editable = ('featured',)

	def base_price_smallest(self, obj):
		price = float(obj.sizes.all()[0].base_price)
		factor = (100 + float(obj.price_factor)) / 100
		size = obj.sizes.all()[0]
		return '%s (%s)' % (float("{0:.2f}".format(price*factor)), str(size))

	base_price_smallest.short_description = 'Base price of smallest volume (excluding promotions)'

	def get_queryset(self, request):
		coffee = super(CoffeeAdmin, self).get_queryset(request)
		coffee = coffee.select_related('roast', 'featured').prefetch_related('sizes')
		return coffee

class CoffeeVolumeAdmin(admin.ModelAdmin):
	list_display = ('__str__','base_price')

class ProductPromotionAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'expired')

	def get_queryset(self, request):
		promotions = super(ProductPromotionAdmin, self).get_queryset(request)
		
		for promotion in promotions:
			if promotion.expiration_date < timezone.now():
				if not promotion.expired:
					promotion.expired = True
					promotion.coffee_set = []
					promotion.merchandise_set = []
					promotion.varietypack_set = []
					promotion.save()

		print len(connection.queries)
		return promotions


	def get_readonly_fields(self, request, obj):
		if obj:
			if obj.expiration_date < timezone.now():
				if not obj.expired:
					obj.expired = True
					obj.coffee_set = []
					obj.merchandise_set = []
					obj.varietypack_set = []
					obj.save()
				
				return ('description', 'discount', 'expiration_date', 'expired')

		print len(connection.queries)
		
		return ('expired',)


class SubscriptionAdmin(admin.ModelAdmin):
	filter_horizontal = ('coffees',)

class MerchandiseAdmin(admin.ModelAdmin):
	filter_horizontal = ('sizes',)
	list_display = ('__str__','price', 'featured')
	list_editable = ('featured',)

class VarietyPackAdmin(admin.ModelAdmin):
	form = VarietyPackForm
	filter_horizontal = ('coffees','merchandise')
	list_display = ('__str__','price', 'featured')
	list_editable = ('featured',)


admin.site.register(CoffeeRoast)
admin.site.register(CoffeeGrind)
admin.site.register(CoffeeVolume, CoffeeVolumeAdmin)
admin.site.register(ShirtSize)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(VarietyPack, VarietyPackAdmin)
admin.site.register(ProductPromotion, ProductPromotionAdmin)


