#Customer Model
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class DiscountRate(models.Model):
	discount_percentage = models.PositiveSmallIntegerField(help_text = 'Percentage discount customer will receive on all coffee orders.')

class Customer(models.Model):
	user = models.OneToOneField(User, blank = True, null = True)
	phone_number = models.CharField(max_length = 24)
	address_1 = models.TextField()
	address_2 = models.TextField(blank=True)
	city = models.CharField(max_length = 32)
	state = models.CharField(max_length = 24)
	zip_code = models.CharField(max_length = 5)
	discount_rate = models.ForeignKey(DiscountRate, blank = True, null = True, on_delete = models.SET_NULL)

	def __str__(self):
		return(self.address_1)