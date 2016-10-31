from __future__ import unicode_literals

from django.db import models

from ..website.models import Timestamp

# Create your models here.

class BlogPost(Timestamp):
	title = models.CharField(max_length=150)
	text = models.TextField()	
	url = models.URLField(blank = True, help_text = 'Add an optional off-site URL.')
	image_url = models.URLField(help_text = 'Link the image that you would like at the head of the post from Amazon S3.')
	old_created_at = models.DateField('Date of previous publication', blank=True, null=True, help_text="YYYY-MM-DD. Leave field blank if this is a new post.")

	def __str__(self):
		return (self.title)

	class Meta:
		verbose_name = "Blog Post"
