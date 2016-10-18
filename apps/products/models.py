from __future__ import unicode_literals

from django.db import models
from ..website.models import Timestamp

# Create your models here.

class Roast(Timestamp):

	name = models.CharField(max_length=48, help_text='Do not ')
	origin = models.CharField(max)
