from django.contrib import admin
from django.utils.html import format_html

from .models import CustomerOrder, ShippingFee, SubscriptionOrder
from .forms import ShippingFeeForm

import datetime
import json
# Register your models here.

class ShippingFeeAdmin(admin.ModelAdmin):
	list_display = ('__str__',)
	form = ShippingFeeForm


class CustomerOrderAdmin(admin.ModelAdmin):
	list_display = ('order_date','order_id', 'billing_info', 'customer', 'ship_to', 'totalItems', 'items')
	search_fields = ['id', 'customer__id', 'customer__user__first_name', 'customer__user__last_name', 'customer__name', 'shipping_address']
	list_filter = ('customer__user__email',)
	list_per_page = 10
	date_hierarchy = 'created_at'


	def get_readonly_fields(self, request, obj):
		return [field.name for field in self.model._meta.fields]

	def order_date(self, obj):
		date = obj.created_at.strftime("%b %d, %Y %H:%M %Z")
		return date

	def order_id(self, obj):
		return obj.id

	def billing_info(self, obj):
		link = format_html("<a href='https://dashboard.stripe.com/test/payments/%s' target='_blank'>Billing Info</a>" % (obj.charge_id,))
		return link

	def has_add_permission (self, request):
		return False

	# def has_delete_permission(self, request, obj=None):
	# 	return False

	def ship_to(self, obj):
		return format_html(obj.parse_shipping_address())

	

	def items(self, obj):
		result = ''
		if obj.coffee:
			result += obj.parse_coffee()

		if obj.merch:
			result += obj.parse_merchandise()

		return format_html(result)


	order_date.short_description = "Order Date (UTC)"

class SubscriptionOrderAdmin(admin.ModelAdmin):
	list_display = ('products', 'subscription', 'activation_date', 'status', 'subscription_num', 'subscription_info', 'customer', 'ship_to')
	search_fields = ['id', 'customer__id', 'customer__user__first_name', 'customer__user__last_name', 'customer__name', 'shipping_address']
	list_filter = ('customer__user__email', 'status',)
	list_per_page = 10
	date_hierarchy = 'created_at'

	def get_readonly_fields(self, request, obj):
		return [field.name for field in self.model._meta.fields]

	def activation_date(self, obj):
		date = obj.created_at.strftime("%b %d, %Y %H:%M %Z")
		return date

	def subscription_num(self, obj):
		return obj.id
	def subscription_info(self, obj):
		link = format_html("<a href='https://dashboard.stripe.com/test/subscriptions/%s' target='_blank'>Subscription Info</a>" % (obj.stripe_id,))
		return link
	def ship_to(self, obj):
		return format_html(obj.parse_shipping_address())
	def products(self, obj):
		return '%sx %s bag(s) of %s %s' % (obj.quantity, obj.size, obj.coffee, obj.grind)

	activation_date.short_description = "Activation Date (UTC)"

admin.site.register(CustomerOrder, CustomerOrderAdmin)
admin.site.register(ShippingFee, ShippingFeeAdmin)
admin.site.register(SubscriptionOrder, SubscriptionOrderAdmin)
