from __future__ import unicode_literals

from django.db import models

from ..customers.models import Customer
from ..products.models import Coffee, Merchandise, Subscription, VarietyPack, Coupon


import json


# Create your models here.

class CustomerOrder(models.Model):
	charge_id = models.CharField(max_length=40)
	coffee = models.TextField(blank=True)
	subscriptions = models.TextField(blank=True)
	merch = models.TextField(blank=True)
	customer = models.ForeignKey(Customer)
	coupon = models.ForeignKey(Coupon, blank = True, null = True, on_delete = models.SET_NULL)
	totalPrice = models.FloatField('Total Price')
	totalItems = models.PositiveSmallIntegerField('Total Items')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.customer)


	def migrate_data(self, shoppingCart, customer):
		self.coffee = json.dumps(shoppingCart['coffee']) if len(shoppingCart['coffee']) > 0 else ""
		self.merch = json.dumps(shoppingCart['merch']) if len(shoppingCart['merch']) > 0 else ""
		self.subscriptions = json.dumps(shoppingCart['subscriptions']) if len(shoppingCart['subscriptions']) > 0 else ""
		self.customer = customer
		self.totalPrice = shoppingCart['totalPrice']
		self.totalItems = shoppingCart['totalItems']

	def parse_coffee(self, as_json=False):
		if not self.coffee:
			return ''

		data = json.loads(self.coffee)

		if as_json:
			result = []

			for coffee in data:
				obj = {}
				obj['qty'] = coffee['qty']
				obj['size'] = coffee['size']['qty']
				obj['name'] = coffee['name']
				obj['grind'] = coffee['grind']['name']
				result.append(json.dumps(obj))

			return result

		result = ''

		for coffee in data:
			result += "Qty: %s (%s) -  %s %s<br><br>" % (coffee['qty'], coffee['size']['qty'], coffee['name'], coffee['grind']['name'])

		return result

	def parse_merchandise(self, as_json=False):
		if not self.merch:
			return ''

		data = json.loads(self.merch)

		if as_json:
			result = []

			for merch in data:
				obj = {}
				obj['qty'] = merch['qty']
				obj['name'] = merch['name']
				if merch.get('size'):
					obj['shirt_size'] = merch['size']['size']

				coffees = merch.get('coffee')
				if coffees is not None:
					obj['coffee'] = []

					if type(coffees) is list:
						for coffee in coffees:
							obj['coffee'].append({'name':coffee['name'], 'grind':merch['grind']['name']})
					else:
						obj['coffee'].append({'name':coffees['name'], 'grind':merch['grind']['name']})
				result.append(json.dumps(obj))

			return result

		result = ''

		for merch in data:
			result += 'Qty: %s - %s' % (merch['qty'], merch['name'])
			if merch.get('size'):
				result += "<br>&nbsp;&nbsp;Shirt Size: %s" % (merch['size']['size'],)

			coffees = merch.get('coffee')
			if coffees is not None:
				result += "<br>&nbsp;&nbsp;Coffee: <ul>"

				if type(coffees) is list:					
					for coffee in coffees:
						result += "<li>%s - %s</li>" % (coffee['name'], merch['grind']['name'])
				else:
					result += "<li>%s - %s</li>" % (coffees['name'], merch['grind']['name'])
				result += "</ul>"
			result += '<br><br>'
		
		return result

	def serialize_model(self):
		return {
			'coffee' : self.coffee,
			'merch' : self.merch,
			'subscriptions' : self.subscriptions,
			'customer' : self.customer.shipping_address(False, True),
			'id' : self.id,
			'created_at' : self.created_at,
			'coupon' : {
				'code' : self.coupon.code,
				'discount' : self.coupon.discount,
			},
			'discount_rate' : self.customer.discount_rate.discount_percentage,
			'totalPrice' : self.totalPrice,
			'totalItems' : self.totalItems

		}











