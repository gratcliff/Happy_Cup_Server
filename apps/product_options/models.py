from __future__ import unicode_literals

from django.db import models

from ..website.models import Timestamp, PriceTimestamp

# Create your models here.

class CoffeeRoast(Timestamp):

	name = models.CharField('Type of roast (i.e. Medium, Dark, Single Origin)',max_length=24, help_text='Do not include "Roast" in the name')
	origin = models.CharField('Country of origin (if Single Origin)', max_length=24, blank=True, help_text='Leave blank if not Single Origin')


	def __str__(self):

		if self.origin == '':
			return '%s Roast' % (self.name)

		return '%s - %s' % (self.name, self.origin)


class CoffeeGrind(Timestamp):

	name = models.CharField('Type of Grind', unique=True, max_length=48)

	def __str__(self):
		return self.name

class CoffeeVolume(PriceTimestamp):

	POUNDS = 'lbs'
	OUNCES = 'oz'

	UNIT_CHOICES = (
		(OUNCES, 'Ounces'),
		(POUNDS, 'Pounds')
	)

	unit = models.CharField('Unit of Measurment', max_length=3, choices=UNIT_CHOICES, default=OUNCES)
	qty = models.PositiveSmallIntegerField('Number of units')
	base_price = models.DecimalField('Base price (dollars) for any coffee at this weight', max_digits=5, decimal_places=2)


	def __str__(self):
		return '%s%s' % (str(self.qty), self.unit)

	class Meta:
		ordering = ['-unit', 'qty']

class ShirtSize(Timestamp):

	XSMALL = 'XS'
	SMALL = 'S'
	MEDIUM = 'M'
	LARGE = 'L'
	XLARGE = 'XL'
	XXLARGE = '2XL'
	XXXLARGE = '3XL'

	SIZE_CHOICES = (
		(XSMALL, 'X-Small'),
		(SMALL, 'Small'),
		(MEDIUM, 'Medium'),
		(LARGE, 'Large'),
		(XLARGE, 'X-Large'),
		(XXLARGE, '2X-Large'),
		(XXXLARGE, '3X-Large')
	)

	size = models.CharField(max_length=3, choices=SIZE_CHOICES, unique=True)

	def __str__(self):
		return self.size



