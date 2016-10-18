from django.contrib import admin

from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast
from ..products.models import Coffee, FeaturedProduct

# Register your models here.

admin.site.register(CoffeeRoast)
admin.site.register(CoffeeGrind)
admin.site.register(CoffeeVolume)
admin.site.register(Coffee)
admin.site.register(FeaturedProduct)
