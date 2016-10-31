from __future__ import unicode_literals

from django.db import models


from ..website.models import Timestamp



# Create your models here.

class FullWidthSection(Timestamp):
	image_url = models.URLField(help_text = "Link the image that you would like displayed in a large section from Amazon S3.")
	header = models.CharField(max_length=32)
	first_paragraph = models.TextField()
	second_paragraph = models.TextField(blank=True, help_text = 'Use this field if you would like a break(space) between text.')

	def __str__(self):
		return (self.header)


class StaffMemberEntry(Timestamp):
	image_url = models.URLField()
	name = models.CharField(max_length=40)
	position = models.CharField(max_length=24)
	member_story = models.TextField(help_text = 'A short description of the employee.')

	def __str__(self):
		return '%s %s' % (self.name, self.position)
