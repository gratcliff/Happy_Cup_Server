from __future__ import unicode_literals

from django.db import models


from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast, ShirtSize
from ..website.models import PriceTimestamp

from django.utils import timezone


# Create your models here.


class Coupon(models.Model):
	code = models.CharField(max_length = 24)
	discount = models.PositiveSmallIntegerField('Percent discount', default=15, help_text='Positive, whole numbers only')
	expiration_date = models.DateTimeField('Date and time that promotion ends', help_text='Server timezone is UTC (Coordinated Universal Time)')
	created_at = models.DateTimeField(auto_now = True)
	updated_at = models.DateTimeField(auto_now_add = True)

class Coffee(PriceTimestamp):

	name = models.CharField(max_length=24)
	roast = models.ForeignKey(CoffeeRoast)
	grinds = models.ManyToManyField(CoffeeGrind)
	sizes = models.ManyToManyField(CoffeeVolume)
	description = models.TextField()
	image_url = models.URLField()
	price_factor = models.SmallIntegerField('Increase or decrease the base price by the following percentage.  Use negative values to decrease price.', default=0)
	featured = models.ForeignKey('ProductPromotion', verbose_name="To feature this product, select a promotional deal.", blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to = {'expired' : False})

	def __str__(self):
		return '%s %s' % (self.name, self.roast)

class Subscription(PriceTimestamp):

	frequency = models.PositiveSmallIntegerField('Number of weeks between each shipment')
	coffees = models.ManyToManyField(Coffee)
	price = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return '%s Week Subscription' % (self.frequency,)

class Merchandise(PriceTimestamp):

	name = models.CharField(max_length=24)
	description = models.TextField()
	image_url = models.URLField()
	sizes = models.ManyToManyField(ShirtSize, verbose_name='Shirt Sizes available (if applicable)', blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	featured = models.ForeignKey('ProductPromotion', verbose_name="To feature this product, select a promotional deal.", blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to = {'expired' : False})

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Merchandise"

class VarietyPack(PriceTimestamp):
	name = models.CharField(max_length=24)
	description = models.TextField()
	image_url = models.URLField()
	coffee_qty = models.PositiveSmallIntegerField('Number of bags of coffee in variety pack (if applicable)', default=0)
	coffees = models.ManyToManyField(Coffee, verbose_name='Coffees in variety pack (if applicable)', blank=True)
	merchandise = models.ManyToManyField('Merchandise', verbose_name='Merchandise in variety pack (if applicable)', blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	featured = models.ForeignKey('ProductPromotion', verbose_name="To feature this product, select a promotional deal.", blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to = {'expired' : False})

	def __str__(self):
		return self.name

class ProductPromotion(PriceTimestamp):

	description = models.CharField(max_length=64)
	discount = models.PositiveSmallIntegerField('Percent discount', default=15, help_text='Positive, whole numbers only')
	expiration_date = models.DateTimeField('Date and time that promotion ends', help_text='Server timezone is UTC (Coordinated Universal Time)')
	expired = models.BooleanField(default=False)

	def __str__(self):
		return '%s (%s percent)' % (self.description, self.discount)











