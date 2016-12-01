from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


from ..product_options.models import CoffeeVolume, CoffeeGrind, CoffeeRoast, ShirtSize
from ..website.models import PriceTimestamp, Timestamp

import stripe


# Create your models here.


class Coupon(models.Model):
	code = models.CharField(max_length = 24, unique=True)
	discount = models.PositiveSmallIntegerField('Percent discount', default=15, help_text='Positive, whole numbers only')
	expiration_date = models.DateTimeField('Date and time that coupon stops working', help_text='Server timezone is UTC (Coordinated Universal Time)')
	created_at = models.DateTimeField(auto_now = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return "%s (%s percent off)" % (self.code, self.discount)

	def is_valid_coupon(self):
		return self.expiration_date > timezone.now()

class Coffee(Timestamp):

	name = models.CharField(max_length=24)
	roast = models.ForeignKey(CoffeeRoast)
	wholesale = models.BooleanField(default=False, help_text="Check this if coffee is only sold in wholesale volumes.")
	grinds = models.ManyToManyField(CoffeeGrind)
	sizes = models.ManyToManyField(CoffeeVolume)
	description = models.TextField(blank=True)
	image_url = models.URLField(blank=True)
	price_factor = models.SmallIntegerField('Increase or decrease the base price by the following percentage.  Use negative values to decrease price.', default=0)
	featured = models.ForeignKey('ProductPromotion', verbose_name="To feature this product, select a promotional deal.", blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to = {'expired' : False})
	

	def __str__(self):
		return self.name

class Subscription(Timestamp):

	frequency = models.PositiveSmallIntegerField('Number of weeks between each shipment', unique=True)
	coffees = models.ManyToManyField(Coffee, blank=True)
	description = models.TextField(blank=True)
	image_url = models.URLField(blank=True)

	def __str__(self):
		return '%s Week Plan' % (self.frequency,)

	def create_or_retreive_plan(self, price, shipping_fee):
		price = price*100
		shipping_fee = shipping_fee*100
		price_int = int(price+shipping_fee)
		plan_id = "%s-week-plan-%s" % (self.frequency, str(price_int))


		try:
			plan = stripe.Plan.retrieve(plan_id)
			return plan
		except Exception as e:
			print e.args, 'line 64 products models'

			try:
				plan = stripe.Plan.create(
					amount = price_int,
					name = "%s Week Plan at $%s" % (self.frequency, str(price_int/100.0)),
					interval = 'week',
					interval_count = self.frequency,
					currency = 'usd',
					id = plan_id
				)
				return plan
			except Exception as e:
				print e.args, 'line76 products models'
				return {'api_error': str(e)}



class Merchandise(Timestamp):

	name = models.CharField(max_length=24)
	description = models.TextField(blank=True)
	image_url = models.URLField(blank=True)
	sizes = models.ManyToManyField(ShirtSize, verbose_name='Shirt Sizes available (if applicable)', blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	featured = models.ForeignKey('ProductPromotion', verbose_name="To feature this product, select a promotional deal.", blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to = {'expired' : False})
	ship_wt = models.DecimalField('Shipping Weight', max_digits=4, decimal_places=2)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Merchandise"

class VarietyPack(Timestamp):
	name = models.CharField(max_length=24)
	description = models.TextField(blank=True)
	image_url = models.URLField(blank=True)
	coffee_qty = models.PositiveSmallIntegerField('Number of bags of coffee in variety pack (if applicable)', default=0)
	coffees = models.ManyToManyField(Coffee, verbose_name='Coffees in variety pack (if applicable)', blank=True)
	merchandise = models.ManyToManyField('Merchandise', verbose_name='Merchandise in variety pack (if applicable)', blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	featured = models.ForeignKey('ProductPromotion', verbose_name="To feature this product, select a promotional deal.", blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to = {'expired' : False})
	ship_wt = models.DecimalField('Shipping Weight', max_digits=4, decimal_places=2)

	def __str__(self):
		return self.name

class ProductPromotion(PriceTimestamp):

	description = models.CharField(max_length=64)
	discount = models.PositiveSmallIntegerField('Percent discount', default=15, help_text='Positive, whole numbers only')
	display = models.BooleanField('Display in Featured Section?', default=True, help_text="If this is unchecked, products under this promotion will not be displayed in the featured products section.")
	expiration_date = models.DateTimeField('Date and time that promotion ends', help_text='Server timezone is UTC (Coordinated Universal Time)')
	expired = models.BooleanField(default=False)

	def __str__(self):
		return self.description











