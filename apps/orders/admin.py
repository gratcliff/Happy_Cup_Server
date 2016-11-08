from django.contrib import admin
from django.utils.html import format_html

from .models import CustomerOrder

import datetime
import json
# Register your models here.


class CustomerOrderAdmin(admin.ModelAdmin):
	list_display = ('order_date','order_id', 'billing_info', 'customer', 'shipping_address', 'totalItems', 'items')
	search_fields = ['id', 'customer__name']
	list_filter = ('created_at',)
	list_per_page = 10


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

	def has_delete_permission(self, request, obj=None):
		return False

	def shipping_address(self, obj):
		return format_html(obj.customer.shipping_address())

	

	def items(self, obj):
		result = ''
		if obj.coffee:
			result += obj.parse_coffee()

		if obj.merch:
			result += obj.parse_merchandise()

		return format_html(result)


	order_date.short_description = "Order Date (UTC)"

admin.site.register(CustomerOrder, CustomerOrderAdmin)
