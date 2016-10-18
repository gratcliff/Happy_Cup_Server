from __future__ import unicode_literals

from django.db import models

from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast
from ..website.models import Timestamp


# Create your models here.

class Coffee(Timestamp):

	name = models.CharField(max_length=24)
	roast = models.ForeignKey(CoffeeRoast)
	grinds = models.ManyToManyField(CoffeeGrind)
	sizes = models.ManyToManyField(CoffeeVolume)
	description = models.TextField()
	image_url = models.URLField()
	price_factor = models.SmallIntegerField('Increase or decrease the base price by the following percentage.  Use negative values to decrease price.', default=0)

	def __str__(self):
		return '%s %s' % (self.name, self.roast)

class FeaturedProduct(Timestamp):

	description = models.CharField(max_length=64)
	discount = models.PositiveSmallIntegerField('Percent discount', default=15, help_text='Positive, whole numbers only')
	expiration_date = models.DateTimeField('Date and time that promotion ends')
	coffees = models.ManyToManyField(Coffee)

	def __str__(self):
		return '%s (%s)' % (self.description, self.discount)


