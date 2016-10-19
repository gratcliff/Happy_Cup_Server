from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast
from ..products.models import Coffee, FeaturedProduct


class QuerySet(object):

	def __init__(self):

		self.coffee = Coffee.objects.all().select_related('roast').prefetch_related('grinds', 'sizes')