from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast
from ..products.models import Coffee, Subscription, Merchandise, VarietyPack, ProductPromotion

from django.utils import timezone


class QuerySet(object):

	def __init__(self):

		self.coffee = Coffee.objects.all().select_related('roast','featured').prefetch_related('grinds', 'sizes')
		self.subscriptions = Subscription.objects.all().prefetch_related('coffees')
		self.merchandise = Merchandise.objects.all().select_related('featured').prefetch_related('sizes')
		self.variety_pack = VarietyPack.objects.all().select_related('featured').prefetch_related('coffees', 'merchandise', 'merchandise__sizes', 'coffees__grinds', 'coffees__sizes', 'coffees__roast')
		self.expired_promotions = ProductPromotion.objects.filter(expiration_date__lt=timezone.now())