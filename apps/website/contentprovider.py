from querysets import QuerySet
import serialize


class ContentProvider(object):

	def __init__(self):
		self.query_set = QuerySet()
		self.json_serializer = serialize.JsonSerializer()
		self.coffee_json = []
		self.merchandise_json = []
		self.variety_pack_json = []


	def populate_products(self):

		self.featured_products = []

		(self.coffee_json, self.featured_coffee) = self.json_serializer.serialize_coffee(self.query_set.coffee)

		(self.merchandise_json, self.featured_merchandise) = self.json_serializer.serialize_merch(self.query_set.merchandise)

		(self.variety_pack_json, self.featured_variety) = self.json_serializer.serialize_variety(self.query_set.variety_pack)

		# concatenate merchandise and variety pack lists
		self.merchandise_json.extend(self.variety_pack_json)

		# concatenate each featured product list
		self.featured_products.extend(self.featured_coffee)
		self.featured_products.extend(self.featured_merchandise)
		self.featured_products.extend(self.featured_variety)

	def expired_promotion_check(self):

		self.json_serializer.featured_product_expiration(self.query_set.expired_promotions)






