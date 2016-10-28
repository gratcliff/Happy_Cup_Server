from __future__ import unicode_literals

from django.db import models

from ..website.models import Timestamp

# Create your models here.

class Location(Timestamp):
	name = models.CharField(max_length=36)
	type = models.CharField(max_length=36)
	address = models.TextField()
	number = models.IntegerField()
	url = models.URLField()
	lat = models.FloatField()
	lng = models.FloatField()

	def __str__(self):
		return (self.name)