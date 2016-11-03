from __future__ import unicode_literals

from django.db import models

from ..customers.models import Customer
from ..products.models import Coffee, Merchandise, Subscription, VarietyPack, Coupon

# Create your models here.

class CustomerOrder(models.Model):
	coffee = models.TextField()
	subscriptions = models.TextField()
	merch = models.TextField()
	customer = models.OneToOneField(Customer)
	coupon = models.ForeignKey(Coupon, blank = True, null = True, on_delete = models.SET_NULL)
	totalPrice = models.FloatField()
	totalItems = models.PositiveSmallIntegerField()
	created_at = models.DateTimeField(auto_now = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return (self.customer, self.created_at)
