#Customer Model
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class DiscountRate(models.Model):
	discount_percentage = models.PositiveSmallIntegerField(help_text = 'Percentage discount customer will receive on all coffee orders.')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.discount_percentage

class Customer(models.Model):
	user = models.OneToOneField(User, blank = True, null = True, limit_choices_to={'is_staff':False})
	discount_rate = models.ForeignKey(DiscountRate, blank = True, null = True, on_delete = models.SET_NULL, help_text="Leave blank for no discount")
	name = models.CharField(max_length=64, blank=True)
	email = models.EmailField(max_length = 128)
	phone_number = models.CharField(max_length = 24)
	address = models.TextField()
	address2 = models.TextField(blank=True)
	city = models.CharField(max_length = 32)
	state = models.CharField(max_length = 32)
	zipcode = models.CharField(max_length = 10)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		if self.user is None:
			return 'Unregistered id: %s' % self.id
		return '%s, Customer ID: %s' % (str(self.user), self.id)

	def shipping_address(self, no_html=False, as_json=False):
		if no_html:
			if self.address2:
				return "%s : %s %s, %s, %s %s" % (self.name, self.address, self.address2, self.city, self.state, self.zipcode)

			return "%s : %s, %s, %s %s" % (self.name, self.address, self.city, self.state, self.zipcode)

		if as_json:
			return { 
				'address': {
					'line1': self.address,
					'line2': self.address2,
					'city': self.city,
					'state': self.state,
					'postal_code': self.zipcode
				},
				'name': self.name,
				'phone': self.phone_number,
				'email': self.email
			}


		if self.address2:
			return "%s<br>%s %s<br>%s, %s %s" % (self.name, self.address, self.address2, self.city, self.state, self.zipcode)

		return "%s<br>%s<br>%s, %s %s" % (self.name, self.address, self.city, self.state, self.zipcode)

	def migrate_data(self, shoppingCart, return_data=False):
		self.name = "%s %s" % (shoppingCart['shipping']['first_name'], shoppingCart['shipping']['last_name'])
		self.email = shoppingCart['shipping']['email']
		self.phone_number = shoppingCart['shipping']['phone_number']
		self.address = shoppingCart['shipping']['address']
		self.address2 = shoppingCart['shipping']['address2'] if 'address2' in shoppingCart['shipping'] else ''
		self.city = shoppingCart['shipping']['city']
		self.state = shoppingCart['shipping']['state']
		self.zipcode = shoppingCart['shipping']['zipcode']

		if return_data:
			return { 'address': {
					'line1': self.address,
					'line2': self.address2,
					'city': self.city,
					'state': self.state,
					'postal_code': self.zipcode
				},
				'name': self.name,
				'phone': self.phone_number,
			}


