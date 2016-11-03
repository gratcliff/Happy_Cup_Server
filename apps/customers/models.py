#Customer Model
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class DiscountRate(models.Model):
	discount_percentage = models.PositiveSmallIntegerField(help_text = 'Percentage discount customer will receive on all coffee orders.')
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.discount_percentage

class Customer(models.Model):
	user = models.OneToOneField(User, blank = True, null = True)
	discount_rate = models.ForeignKey(DiscountRate, blank = True, null = True, on_delete = models.SET_NULL, help_text="Leave blank for no discount")
	shippingemail = models.EmailField(max_length = 128)
	shippingTel = models.CharField(max_length = 24)
	shippingAddress1 = models.TextField()
	shippingAddress2 = models.TextField(blank=True)
	shippingCity = models.CharField(max_length = 32)
	shippingState = models.CharField(max_length = 32)
	shippingPostalCode = models.CharField(max_length = 10)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s, Discount: %s' % (self.user, self.discount_rate)