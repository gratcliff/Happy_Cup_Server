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


def empty_all_carts():
	query = Session.objects.all()
	
	for session in query:
		decode = session.get_decoded()
		if decode.get('shoppingCart') is not None:
			data = SessionStore(session_key=session.session_key)
			data['shoppingCart'] = None
			data.save()

