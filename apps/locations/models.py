from __future__ import unicode_literals

from django.db import models

from ..website.models import Timestamp

# Create your models here.

class StoreType(Timestamp):
	type = models.CharField(max_length=36, unique=True)

	def __str__(self):
		return self.type

class Location(Timestamp):
	name = models.CharField(max_length=36)
	type = models.ForeignKey(StoreType, help_text = 'Choose the type of store associated with the location.')
	address = models.TextField()
	phone_number = models.PositiveIntegerField(help_text="Format must be Area Code + Phone Number (Numbers only)")
	url = models.URLField()
	lng = models.FloatField(verbose_name='Longitude', help_text='Leave this field blank.  Data will be aquired automatically from Google Maps', blank=True, null=True)
	lat = models.FloatField(verbose_name='Latitude', help_text='Leave this field blank.  Data will be aquired automatically from Google Maps', blank=True, null=True)

	def __str__(self):
		return ('%s: %s') % (self.name, self.type)