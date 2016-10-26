from __future__ import unicode_literals

from django.db import models

import serialize

# Create your models here.

class Timestamp(models.Model):

	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

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

