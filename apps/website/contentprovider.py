from querysets import QuerySet
from ..locations.mapsapi import geocode_data

from django.utils import timezone

import serialize



class ContentProvider(object):

	def __init__(self):
		self.query_set = QuerySet()
		self.json_serializer = serialize.JsonSerializer()
		self.coffee_json = []
		self.merchandise_json = []
		self.variety_pack_json = []
		self.about_fullWidthSection = []
		self.about_staffMemberEntry = []
		self.locations = []
		self.blogPosts = []


	def populate_products(self):

		self.featured_products = []

		(self.coffee_json, self.featured_coffee) = self.json_serializer.serialize_coffee(self.query_set.coffee)

		self.subscription_json = self.json_serializer.serialize_subscriptions(self.query_set.subscriptions)

		(self.merchandise_json, self.featured_merchandise) = self.json_serializer.serialize_merch(self.query_set.merchandise)

		(self.variety_pack_json, self.featured_variety) = self.json_serializer.serialize_variety(self.query_set.variety_pack)

		# concatenate merchandise and variety pack lists
		self.merchandise_json.extend(self.variety_pack_json)

		# concatenate each featured product list
		self.featured_products.extend(self.featured_coffee)
		self.featured_products.extend(self.featured_merchandise)
		self.featured_products.extend(self.featured_variety)

	def populate_aboutPage(self):
		self.about_fullWidthSection = self.json_serializer.serialize_fullWidthSections(self.query_set.fullWidthSection)
		self.about_staffMemberEntry = self.json_serializer.serialize_staffMemberEntry(self.query_set.staffMemberEntry)

	def populate_locations(self):
		self.locations = self.json_serializer.serialize_locations(self.query_set.location)

	def populate_news(self):
		self.blogPosts = self.json_serializer.serialize_blogPosts(self.query_set.blogPost)

	def expired_promotion_check(self):
		self.json_serializer.featured_product_expiration(self.query_set.expired_promotions)

	def refresh_geocodes(self):
		location = self.query_set.refresh_geocodes

		if location:

			cleaned_data = {
				'address' : location.address,
				'lat' : location.lat,
				'lng' : location.lng
			}

			new_data = geocode_data(cleaned_data)
			if 'error' not in new_data:
				if new_data['address'] == cleaned_data['address'] and new_data['lat'] == cleaned_data['lat'] and new_data['lng'] == cleaned_data['lng']:
					location.updated_at = timezone.now()
					location.save()
					serialize.db_modified = False
				else:
					location.lat = new_data['lat']
					location.lng = new_data['lng']
					location.address = new_data['address']
					location.updated_at = timezone.now()
					location.save()







