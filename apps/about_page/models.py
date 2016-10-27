from __future__ import unicode_literals

from django.db import models


from ..website.models import Timestamp



# Create your models here.

class FullWidthSection(Timestamp):
	image_url = models.URLField()
	header = models.CharField(max_length=32)
	first_paragraph = models.TextField()
	second_paragraph = models.TextField(blank=True)

	def __str__(self):
		return (self.header)


class StaffMemberEntry(Timestamp):
	image_url = models.URLField()
	name = models.CharField(max_length=40)
	position = models.CharField(max_length=24)
	member_story = models.TextField()

	def __str__(self):
		return (self.name, self.position)
