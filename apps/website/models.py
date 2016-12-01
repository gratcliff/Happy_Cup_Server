from __future__ import unicode_literals

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from django.db import models
import serialize



# Create your models here.

class Timestamp(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def save(self, *args, **kwargs):

		# modifies save() in order to tell the server that query_sets
		# must be refreshed so that updated data is sent to the front end

		serialize.db_modified = True


		super(Timestamp, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):

		# modifies delete() in order to tell the server that query_sets
		# must be refreshed so that updated data is sent to the front end

		serialize.db_modified = True


		super(Timestamp, self).delete(*args, **kwargs)


class PriceTimestamp(models.Model):

	""" Similar to Timestamp class, except it will be inherited by models that affect product pricing """

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def save(self, *args, **kwargs):

		# modifies save() in order to tell the server that query_sets
		# must be refreshed so that updated data is sent to the front end

		serialize.db_modified = True
		empty_all_carts()


		super(PriceTimestamp, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):

		# modifies delete() in order to tell the server that query_sets
		# must be refreshed so that updated data is sent to the front end

		serialize.db_modified = True
		empty_all_carts()


		super(PriceTimestamp, self).delete(*args, **kwargs)


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

class ContactPage(Timestamp):

	image_url = models.URLField('Image on page top',help_text="Link from Amazon S3. To ensure proper styling, image should be no smaller than 945 pixels wide and 532 pixels high.", blank=True)
	roaster_line1 = models.CharField('Happy Cup Roaster: Line 1', max_length=32,blank=True)
	roaster_line2 = models.CharField('Happy Cup Roaster: Line 2', max_length=32,blank=True)
	account_line1 = models.CharField('Account Questions: Line 1', max_length=32,blank=True)
	account_line2 = models.CharField('Account Questions: Line 2', max_length=32,blank=True)
	account_line3 = models.CharField('Account Questions: Line 3', max_length=32,blank=True)
	billing_line1 = models.CharField('Billing Questions: Line 1', max_length=32,blank=True)
	billing_line2 = models.CharField('Billing Questions: Line 2', max_length=32,blank=True)
	billing_line3 = models.CharField('Billing Questions: Line 3', max_length=32,blank=True)
	media_kit_url = models.URLField(help_text='Link from Amazon S3', blank=True)

	def __str__(self):
		return 'Contact Page Content'


	def serialize_model(self):
		return {
			'image_url' : self.image_url,
			'roaster_line1' : self.roaster_line1,
			'roaster_line2' : self.roaster_line2,
			'account_line1' : self.account_line1,
			'account_line2' : self.account_line2,
			'account_line3' : self.account_line3,
			'billing_line1' : self.billing_line1,
			'billing_line2' : self.billing_line2,
			'billing_line3' : self.billing_line3,
			'media_kit_url' : self.media_kit_url
		}



def empty_all_carts():
	query = Session.objects.all()
	
	for session in query:
		decode = session.get_decoded()
		if decode.get('shoppingCart') is not None:
			data = SessionStore(session_key=session.session_key)
			data['shoppingCart'] = None
			data.save()

