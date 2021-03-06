#Customer Model
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import stripe
import time




# Create your models here.
class WholesalePrice(models.Model):
	discount_rate = models.PositiveSmallIntegerField('Percent discount', help_text="Specific customers will receive this discount on wholesale volumes.", unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Wholesale Price Discount'

	def __str__(self):
		return "%s percent" % (str(self.discount_rate),)

class Customer(models.Model):
	user = models.OneToOneField(User, blank = True, null = True, limit_choices_to={'customer': None})
	stripe_id = models.TextField(blank=True)
	wholesale_price = models.ForeignKey(WholesalePrice, blank = True, null = True, on_delete = models.SET_NULL, help_text="Leave blank to use default price")
	name = models.CharField(max_length=64, blank=True)
	email = models.EmailField(max_length = 128, blank=True)
	phone_number = models.CharField(max_length = 24, blank=True)
	address = models.TextField(blank=True)
	address2 = models.TextField(blank=True)
	city = models.CharField(max_length = 32, blank=True)
	state = models.CharField(max_length = 32, blank=True)
	zipcode = models.CharField(max_length = 10, blank=True)
	registered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		if self.user is None:
			return 'Customer ID: %s' % self.id
		return '%s %s (%s), Customer ID: %s' % (self.user.first_name, self.user.last_name, self.user.email, self.id)

	def create_or_retreive_customer(self, source, user):
		
		if self.stripe_id:
			try:
				id_list = self.stripe_id.split(', ')
				for cust_id in id_list:
					if len(id_list) > 1:
						time.sleep(0.1)
					customer = stripe.Customer.retrieve(cust_id)
					for key in customer.sources.get('data'):
						new_customer = False
						if key['last4'] != source['card']['last4']:
							print 'last4'
							new_customer = True
						if key['exp_month'] != source['card']['exp_month']:
							print 'exp_month'
							new_customer = True
						if key['exp_year'] != source['card']['exp_year']:
							print 'exp_year'
							new_customer = True
						if key['address_zip'] != source['card']['address_zip']:
							print 'zip'
							new_customer = True

						if not new_customer:
							print customer
							return customer

			except stripe.error.InvalidRequestError as e:
				print 'invalid request'
				print e.json_body
			except stripe.error.APIConnectionError as e:
				return {'api_error': e.json_body['error']['message']}
			except Exception as e:
				print e.args
				return {'api_error': str(e)}

		try:
			customer = stripe.Customer.create(
				source=source['id'],
				email=user.email,
				description="Customer record for %s %s" % (user.first_name, user.last_name)
			)
			if new_customer:
				self.stripe_id = "%s, %s" % (self.stripe_id, customer['id'])
			else :
				self.stripe_id = customer['id']
			self.save()
			return customer
		except Exception as e:
			print e.args
			return {'api_error': str(e)}


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
				'email': self.email,
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


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer)
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
		unique_together = ('customer', 'name', 'address', 'address2', 'city', 'state', 'zipcode')
		verbose_name_plural = 'Shipping Addresses'

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
				'email': self.email,
				'id' : self.id
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

