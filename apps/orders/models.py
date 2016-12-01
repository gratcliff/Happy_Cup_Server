from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string

from ..customers.models import Customer
from ..products.models import Coffee, Merchandise, Subscription, VarietyPack, Coupon

import json
import math
import stripe


# Create your models here.

class ShippingFee(models.Model):
	min_weight = models.SmallIntegerField('Minimum weight in range',unique=True, help_text="Pounds")
	max_weight = models.SmallIntegerField('Maximum weight in range',unique=True, help_text="Pounds")
	price = models.SmallIntegerField(help_text="Whole Dollars")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ['price']

	def __str__(self):
		return "%s-%slbs : $%s" % (str(self.min_weight), str(self.max_weight), str(self.price))


class CustomerOrder(models.Model):
	charge_id = models.CharField(max_length=40)
	coffee = models.TextField(blank=True)
	subscriptions = models.TextField(blank=True)
	merch = models.TextField(blank=True)
	customer = models.ForeignKey(Customer)
	shipping_address = models.TextField(blank=True)
	shipping_fee = models.PositiveSmallIntegerField(default=0)
	coupon = models.ForeignKey(Coupon, blank = True, null = True, on_delete = models.SET_NULL)
	subTotalPrice = models.FloatField('Price before coupons and shipping', default=0)
	totalPrice = models.FloatField('Total Price')
	totalItems = models.PositiveSmallIntegerField('Total Items')
	other_info = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.customer)

	def parse_shipping_address(self, no_html=False, as_json=False):

		address_json = json.loads(self.shipping_address)

		if no_html:
			if address_json['address']['line2']:
				return "%s : %s %s, %s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['line2'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])

			return "%s : %s, %s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])



		if as_json:
			return address_json


		if address_json['address']['line2']:
			return "%s<br>%s %s<br>%s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['line2'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])

		return "%s<br>%s<br>%s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])


	def migrate_data(self, shoppingCart, customer, coupon, shipping_address):
		self.coffee = json.dumps(shoppingCart['coffee']) if len(shoppingCart['coffee']) > 0 else ""
		self.merch = json.dumps(shoppingCart['merch']) if len(shoppingCart['merch']) > 0 else ""
		self.subscriptions = json.dumps(shoppingCart['subscriptions']) if len(shoppingCart['subscriptions']) > 0 else ""
		self.customer = customer
		self.shipping_address = json.dumps(shipping_address(False, True))
		self.subTotalPrice = shoppingCart['subTotalPrice']
		self.shipping_fee = shoppingCart['shippingFee']
		self.totalPrice = shoppingCart['totalPrice'] + shoppingCart['shippingFee']
		self.totalItems = shoppingCart['totalItems']
		self.other_info = shoppingCart['shipping'].get('message', '')
		self.coupon = coupon

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

	def serialize_model(self, as_json=False):
		obj = {
			'coffee' : self.coffee,
			'merch' : self.merch,
			'subscriptions' : self.subscriptions,
			'customer' : self.customer.id,
			'shipping_address' : self.parse_shipping_address(False, True),
			'id' : self.id,
			'created_at' : self.created_at,
			'coupon' : {
				'code' : self.coupon.code,
				'discount' : self.coupon.discount,
			} if self.coupon else None,
			'wholesale_price' : self.customer.wholesale_price.discount_rate if self.customer.wholesale_price else None,
			'subTotalPrice' : self.subTotalPrice,
			'priceAfterCoupon' : self.totalPrice - self.shipping_fee,
			'shipping_fee' : self.shipping_fee,
			'totalPrice' : self.totalPrice,
			'totalItems' : self.totalItems,
			'other_info' : self.other_info
		}

		if as_json:

			if self.coffee:
				obj['coffee'] = json.loads(obj['coffee'])
			if self.merch:
				obj['merch'] = json.loads(obj['merch'])
				for item in obj['merch']:
					if 'coffee' in item:
						if type(item['coffee']) is not list:
							item['coffee'] = [ item['coffee'] ]

			if self.subscriptions:
				obj['subscriptions'] = json.loads(obj['subscriptions'])

		return obj

	def send_email_confirmation(self, charge):

		build_context = {'charge':{'shipping': charge['shipping'], 'source': charge['source']}}
		build_context['charge']['source']['phone_number'] = charge['metadata'].get('billing_phone')
		build_context['charge']['source']['email'] = charge.get('receipt_email')
		build_context['order'] = self.serialize_model(True)

		message_context = {
			'shipping': build_context['order']['shipping_address'],
			'billing' : build_context['charge']['source'],
			'order': build_context['order']
		}

		subject = "Your Happy Cup Coffee Order"
		recipient = [ build_context['charge']['source']['email'] ]
		from_email = ''
		message = 'Thank you for your order.'
		message_html = render_to_string('orders/email_confirmation.html', message_context)

		send_mail(subject,message,from_email,recipient, html_message=message_html)



class SubscriptionOrder(models.Model):

	stripe_id = models.CharField(max_length=40)
	customer = models.ForeignKey(Customer)
	subscription = models.ForeignKey(Subscription)
	coffee = models.TextField(max_length=24)
	grind = models.CharField(max_length=24)
	size = models.CharField(max_length=8)
	quantity = models.PositiveSmallIntegerField(default=1)
	status = models.CharField(max_length=40, default="active")
	shipping_address = models.TextField(blank=True)
	shipping_fee = models.PositiveSmallIntegerField(default=0)
	subTotalPrice = models.FloatField('Price before shipping', default=0)
	totalPrice = models.FloatField('Total Price')
	other_info = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def create_stripe_subscription(self, customer_id, plan_id, quantity):
		try:
			sub = stripe.Subscription.create(
				customer=customer_id,
				plan=plan_id,
				quantity=quantity
			)
			return sub
		except Exception as e:
			return {'api_error': str(e)}


	def parse_shipping_address(self, no_html=False, as_json=False):

		address_json = json.loads(self.shipping_address)

		if no_html:
			if address_json['address']['line2']:
				return "%s : %s %s, %s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['line2'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])

			return "%s : %s, %s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])



		if as_json:
			return address_json


		if address_json['address']['line2']:
			return "%s<br>%s %s<br>%s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['line2'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])

		return "%s<br>%s<br>%s, %s %s" % (address_json['name'], address_json['address']['line1'], address_json['address']['city'], address_json['address']['state'], address_json['address']['postal_code'])


	def migrate_data(self, stripe_id, subscription, customer, shipping_address, other_info):
		# weight = math.ceil(subscription['ship_wt'])
		# shipping_fee = ShippingFee.objects.filter(min_weight__lte=int(weight), max_weight__gte=int(weight))[0].price

		self.stripe_id = stripe_id
		self.subscription = Subscription.objects.get(id=subscription['id'])
		self.coffee = subscription['coffee']['name']
		self.grind = subscription['grind']['name']
		self.size = subscription['size']['qty']
		self.quantity = subscription['qty']
		self.customer = customer
		self.shipping_address = json.dumps(shipping_address(False, True))
		self.subTotalPrice = subscription['subtotal']
		self.shipping_fee = subscription['shipping_fee'] * self.quantity
		self.totalPrice = subscription['subtotal'] + self.shipping_fee
		self.other_info = other_info

	def serialize_model(self):

		obj = {
			'subscription' : str(self.subscription),
			'subscription_id' : self.subscription.id,
			'coffee' : self.coffee,
			'grind' : self.grind,
			'size' : self.size,
			'quantity' : self.quantity,
			'customer' : self.customer.id,
			'shipping_address' : self.parse_shipping_address(False, True),
			'id' : self.id,
			'created_at' : self.created_at,
			'subTotalPrice' : self.subTotalPrice,
			'shipping_fee' : self.shipping_fee,
			'totalPrice' : self.totalPrice,
			'other_info' : self.other_info,
			'status' : self.status
		}

		return obj

	def send_email_confirmation(self, subscription):

		# build_context = {'charge':{'shipping': self.parse_shipping_address(False, True), 'source': charge['source']}}
		# build_context['charge']['source']['phone_number'] = charge['metadata'].get('billing_phone')
		# build_context['charge']['source']['email'] = charge.get('receipt_email')
		# build_context['order'] = self.serialize_model(True)

		# message_context = {
		# 	'shipping': build_context['order']['shipping_address'],
		# 	'billing' : build_context['charge']['source'],
		# 	'order': build_context['order']
		# }

		subject = "Your Happy Cup Coffee Subscription"
		recipient = [ subscription['billing'][0]['email'] ]
		from_email = ''
		message = """

		Dear %s,
		
		Thank you for subscribing to our %s.
		Subscription # : %s
		Coffee : %s (%s)
		Grind : %s

		Every %s weeks, %s of these bag(s) will be shipped to the following address:

		%s

		Price per shipment is $%s.  A separate email will be sent once payment has been processed.

		

		 """ % (subscription['billing'][0]['name'], str(self.subscription), self.id, self.coffee, self.size, self.grind, self.subscription.frequency, self.quantity, self.parse_shipping_address(True), "{0:.2f}".format(self.totalPrice))

		send_mail(subject,message,from_email,recipient)







