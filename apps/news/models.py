from __future__ import unicode_literals

from django.db import models

from ..website.models import Timestamp

# Create your models here.

class BlogPost(Timestamp, models.Model):
	title = models.CharField(max_length=150)
	link_title = models.TextField()
	description = models.TextField()
	text = models.TextField()
	url = models.URLField()
	image_url = models.URLField()
	

	def __str__(self):
		return (self.title)

	class Meta:
		verbose_name = "Blog Post"
