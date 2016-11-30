from __future__ import unicode_literals

from django.db import models

from ..website.models import Timestamp



# Create your models here.

class CafeCarouselImage(Timestamp):
	image_url = models.URLField(help_text = "Link the image that you would like displayed in a the carousel from Amazon S3.")
	image_alternate_text = models.CharField(max_length=36)
	
	def __str__(self):
		return (self.image_alternate_text)


class Cafe_hours(Timestamp):
	monday_open = models.CharField(max_length=12)
	monday_close = models.CharField(max_length=12)

	tuesday_open = models.CharField(max_length=12)
	tuesday_close = models.CharField(max_length=12)

	wednesday_open = models.CharField(max_length=12)
	wednesday_close = models.CharField(max_length=12)

	thursday_open = models.CharField(max_length=12)
	thursday_close = models.CharField(max_length=12)

	friday_open = models.CharField(max_length=12)
	friday_close = models.CharField(max_length=12)

	saturday_open = models.CharField(max_length=12, blank = True, null = True)
	saturday_close = models.CharField(max_length=12, blank = True, null = True)

	sunday_open = models.CharField(max_length=12, blank = True, null = True)
	sunday_close = models.CharField(max_length=12 , blank = True, null = True)

	class Meta:
		verbose_name_plural = 'Cafe Hours'

	def __str__(self):
		return '%s %s' % (self.monday_open, self.monday_close)

class Cafe_content(Timestamp):
	header = models.CharField(max_length=36)
	description = models.TextField(default= 'Description for Happy Cup Coffee Cafe in Town Hall!')
	address = models.CharField(max_length=36)
	phone_number = models.CharField(max_length=14)
	link_text = models.CharField(max_length=120)
	link_url = models.URLField(help_text= 'Link the document URL from Amazon S3 here.')
	def __str__(self):
		return (self.header) 
