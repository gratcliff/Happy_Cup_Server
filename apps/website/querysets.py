from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast
from ..products.models import Coffee, Subscription, Merchandise, VarietyPack, FeaturedProduct


class QuerySet(object):

	def __init__(self):

		self.coffee = Coffee.objects.all().select_related('roast').prefetch_related('grinds', 'sizes')
		self.subscriptions = Subscription.objects.all().prefetch_related('coffees')
		self.merchandise = Merchandise.objects.all().prefetch_related('sizes')
		self.variety_pack = VarietyPack.objects.all().prefetch_related('coffees', 'merchandise', 'merchandise__sizes', 'coffees__grinds', 'coffees__sizes', 'coffees__roast')