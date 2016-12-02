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
	roaster_address = models.CharField('Happy Cup Roaster\'s Address', max_length=32,blank=True)
	roaster_phone = models.CharField('Happy Cup Roaster\'s Phone', max_length=15,blank=True)
	account_contact = models.CharField('Contact for Account Questions', max_length=32,blank=True)
	account_phone = models.CharField('Account Questions Phone', max_length=15,blank=True)
	account_email = models.EmailField('Account Questions Email', max_length=48,blank=True)
	billing_contact = models.CharField('Contact For Billing Questions', max_length=32,blank=True)
	billing_phone = models.CharField('Billing Questions Phone', max_length=15,blank=True)
	billing_email = models.EmailField('Billing Questions Email', max_length=48,blank=True)
	media_kit_url = models.URLField(help_text='Link from Amazon S3', blank=True)
	hq_address_line1 = models.CharField('Street Address of company headquarters', max_length=32)
	hq_address_line2 = models.CharField('City, State, Zip of company headquarters', max_length=32)
	main_phone = models.CharField("Company\'s primary phone number", max_length=14)

	def __str__(self):
		return 'Contact Page Content'


	def serialize_model(self):
		return {
			'image_url' : self.image_url,
			'roaster_address' : self.roaster_address,
			'roaster_phone' : self.roaster_phone,
			'account_contact' : self.account_contact,
			'account_phone' : self.account_phone,
			'account_email' : self.account_email,
			'billing_contact' : self.billing_contact,
			'billing_phone' : self.billing_phone,
			'billing_email' : self.billing_email,
			'media_kit_url' : self.media_kit_url,
			'hq_address' : '%s %s' % (self.hq_address_line1, self.hq_address_line2),
			'hq_address_line1' : self.hq_address_line1,
			'hq_address_line2' : self.hq_address_line2,
			'main_phone' : self.main_phone
		}



def empty_all_carts():
	query = Session.objects.all()
	
	for session in query:
		decode = session.get_decoded()
		if decode.get('shoppingCart') is not None:
			data = SessionStore(session_key=session.session_key)
			data['shoppingCart'] = None
			data.save()

