from __future__ import unicode_literals

from django.db import models

from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast, ShirtSize
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

class Subscription(Timestamp):

	frequency = models.PositiveSmallIntegerField('Number of weeks between each shipment')
	coffees = models.ManyToManyField(Coffee)
	price = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return '%s Week Subscription' % (self.frequency,)

class Merchandise(Timestamp):

	name = models.CharField(max_length=24)
	description = models.TextField()
	image_url = models.URLField()
	sizes = models.ManyToManyField(ShirtSize, verbose_name='Shirt Sizes available (if applicable)', blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Merchandise"

class VarietyPack(Timestamp):
	name = models.CharField(max_length=24)
	description = models.TextField()
	image_url = models.URLField()
	coffee_qty = models.PositiveSmallIntegerField('Number of bags of coffee in variety pack (if applicable)', default=0)
	coffees = models.ManyToManyField(Coffee, verbose_name='Coffees in variety pack (if applicable)', blank=True)
	merchandise = models.ManyToManyField(Merchandise, verbose_name='Merchandise in variety pack (if applicable)', blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return self.name



class FeaturedProduct(Timestamp):

	description = models.CharField(max_length=64)
	discount = models.PositiveSmallIntegerField('Percent discount', default=15, help_text='Positive, whole numbers only')
	expiration_date = models.DateTimeField('Date and time that promotion ends')
	coffees = models.ManyToManyField(Coffee, blank=True)

	def __str__(self):
		return '%s (%s)' % (self.description, self.discount)




