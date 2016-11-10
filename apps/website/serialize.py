from django.db import connection

db_modified = False
db_price_change = False

class JsonSerializer:

	""" 
		parses though database data so that it
	 is sent to the front end in ideal formats

	"""

	def featured_product_expiration(self, expired_promotions):

		global db_modified

		for promotion in expired_promotions:
			
			if not promotion.expired:
				promotion.coffee_set = []
				promotion.merchandise_set = []
				promotion.varietypack_set = []
				promotion.expired = True
				promotion.save()


	def serialize_wholeSaleCoffee(self, coffees):
		global db_modified

		data = []

		for coffee in coffees:

			obj = {
			'id' : coffee.id,
			'name' : coffee.name,
			'roast' : { 'id' : coffee.roast.id, 'name' : str(coffee.roast) },
			'grinds' : self.serialize_grinds(coffee.grinds.all()),
			'description' : coffee.description,
			'price_per_pound' : coffee.price_per_pound,
			'image_url' : coffee.image_url,
			'type' : 'wholesale'

			}

			data.append(obj)

		db_modified = False

		return data


	def serialize_coffee(self, coffees):

		global db_modified

		data = []
		featured = []

		for coffee in coffees:

			obj = {
				'id' : coffee.id,
				'name' : coffee.name,
				'roast' : { 'id' : coffee.roast.id, 'name' : str(coffee.roast) },
				'grinds' : self.serialize_grinds(coffee.grinds.all()),
				'sizes' : self.serialize_sizes(coffee.sizes.all(), coffee),
				'description' : coffee.description,
				'image_url' : coffee.image_url,
				'price_factor' : coffee.price_factor,
				'type' : 'coffee'
			}


			if coffee.featured is not None:


				obj['featured'] = {
						'id' : coffee.featured.id,
						'description': coffee.featured.description,
						'discount' : coffee.featured.discount, 
						'expiration_date' : coffee.featured.expiration_date
					}

				featured.append(obj)


			data.append(obj)

			

		db_modified = False
		return (data, featured)

	def serialize_grinds(self, grinds):
		data = []

		for grind in grinds:
			obj = {
				'id' : grind.id,
				'name' : str(grind)
			}

			data.append(obj)

		return data


	def serialize_sizes(self, sizes, coffee):
		data = []

		featured_discount = 0 if coffee.featured is None else coffee.featured.discount
		featured_price_factor = (100 + float(coffee.price_factor) - featured_discount) / 100

		for size in sizes:
			obj = {
				'id' : size.id,
				'qty' : str(size),
				'base_price' : float("{0:.2f}".format(float(size.base_price) * featured_price_factor)),
			}

			data.append(obj)

		return data


	def serialize_merch(self, products):
		global db_modified

		data = []
		featured = []

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

			if merch.featured is not None:


				obj['featured'] = {
						'id' : merch.featured.id,
						'description': merch.featured.description,
						'discount' : merch.featured.discount, 
						'expiration_date' : merch.featured.expiration_date
					}
				obj['price'] *= (100-merch.featured.discount) / 100.0
				obj['price'] = float("{0:.2f}".format(obj['price']))

				featured.append(obj)

			data.append(obj)


		db_modified = False
		return (data, featured)


	def serialize_shirt_sizes(self, sizes):

		data = []
		for size in sizes:
			obj = {
				'id' : size.id,
				'size' : str(size.get_size_display()),
			}

			data.append(obj)

		return data if len(data) > 0 else None


	def serialize_variety(self, variety_packs):
		global db_modified

		data = []
		featured = []

		for pack in variety_packs:

			obj = {

				'id' : pack.id,
				'name' : pack.name,
				'description' : pack.description,
				'image_url' : pack.image_url,
				'coffee_qty' : pack.coffee_qty,
				'coffees' : self.serialize_coffee(pack.coffees.all())[0],
				'merchandise' : self.serialize_merch(pack.merchandise.all())[0],
				'price' : float(pack.price),
				'type' : 'variety'

			}

			if pack.featured is not None:


				obj['featured'] = {
						'id' : pack.featured.id,
						'description': pack.featured.description,
						'discount' : pack.featured.discount, 
						'expiration_date' : pack.featured.expiration_date
					}
				obj['price'] *= (100-pack.featured.discount) / 100.0
				obj['price'] = float("{0:.2f}".format(obj['price']))

				featured.append(obj)

			data.append(obj)

		db_modified = False
		return (data, featured)

	def serialize_fullWidthSections(self, sections):
		global db_modified
		data = []

		for section in sections:
			obj = {
				'id': section.id,
				'image_url': section.image_url,
				'header': section.header,
				'first_paragraph': section.first_paragraph,
				'second_paragraph': section.second_paragraph
			}
			data.append(obj)

		db_modified = False
		return data if len(data) > 0 else None

	def serialize_staffMemberEntry(self, staves):
		global db_modified
		data = []

		for staff in staves:
			obj = {
				'id': staff.id,
				'image_url': staff.image_url,
				'name': staff.name,
				'position': staff.position,
				'member_story': staff.member_story
			}
			data.append(obj)

		db_modified = False
		return data if len(data) > 0 else None

	def serialize_locations(self, locations):
		global db_modified
		data = []
		for location in locations:
			obj = {
				'id': location.id,
				'name': location.name,
				'type': location.type.type,
				'address': location.address,
				'phone_number': location.phone_number,
				'url': location.url,
				'lat': location.lat,
				'lng': location.lng
			}
			data.append(obj)

		db_modified = False
		return data if len(data) > 0 else None

	def serialize_blogPosts(self, posts):
		global db_modified
		data = []

		for post in posts:
			obj = {
			'id': post.id,
			'title': post.title,
			'text': post.text,
			'url': post.url,
			'image_url': post.image_url,
			'created_at': post.old_created_at if not None else post.created_at
			}
			data.append(obj)

		db_modified = False
		return data if len(data) > 0 else None



		
		

		
		
			