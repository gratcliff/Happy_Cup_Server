import json
from django.core import serializers

db_modified = False

class JsonSerializer:

	""" 
		parses though database data so that it
	 is sent to the front end in ideal formats

	"""

	def serialize_coffee(self, coffees):

		global db_modified

		data = []

		for coffee in coffees:

			obj = {
				'id' : coffee.id,
				'name' : coffee.name,
				'roast' : { 'id' : coffee.roast.id, 'name' : str(coffee.roast) },
				'grinds' : self.serialize_grinds(coffee.grinds.all()),
				'sizes' : self.serialize_sizes(coffee.sizes.all()),
				'description' : coffee.description,
				'image_url' : coffee.image_url,
				'price_factor' : coffee.price_factor
			}

			data.append(obj)

		db_modified = False
		return data

	def serialize_grinds(self, grinds):
		data = []

		for grind in grinds:
			obj = {
				'id' : grind.id,
				'name' : str(grind)
			}

			data.append(obj)

		return data


	def serialize_sizes(self, sizes):
		data = []
		for size in sizes:
			obj = {
				'id' : size.id,
				'qty' : str(size),
				'base_price' : float(size.base_price)
			}

			data.append(obj)

		return data


	def serialize_merch(self, products):
		global db_modified

		data = []

		for merch in products:

			obj = {
				'id' : merch.id,
				'name' : merch.name,
				'sizes' : self.serialize_shirt_sizes(merch.sizes.all()),
				'description' : merch.description,
				'image_url' : merch.image_url,
				'price' : float(merch.price),
				'type' : 'merchandise'
			}

			data.append(obj)


		db_modified = False
		return data


	def serialize_shirt_sizes(self, sizes):

		data = []
		for size in sizes:
			obj = {
				'id' : size.id,
				'size' : str(size),
			}

			data.append(obj)

		return data


	def serialize_variety(self, variety_packs):
		global db_modified

		data = []

		for pack in variety_packs:

			obj = {

				'id' : pack.id,
				'name' : pack.name,
				'description' : pack.description,
				'image_url' : pack.image_url,
				'coffee_qty' : pack.coffee_qty,
				'coffees' : self.serialize_coffee(pack.coffees.all()),
				'merchandise' : self.serialize_merch(pack.merchandise.all()),
				'price' : float(pack.price),
				'type' : 'variety'

			}

			data.append(obj)

		db_modified = False
		return data

		



		
		

		
		
			