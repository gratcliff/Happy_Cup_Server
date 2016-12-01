from django.db import connection

from ..customers.models import Customer

db_modified = False
db_price_change = False

from django.db import connection

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


	def serialize_coffee(self, coffees, check_featured=True, variety_pack=False, discount=None):

		global db_modified

		data = []
		featured = []

		for coffee in coffees:

			obj = {
				'id' : coffee.id,
				'name' : coffee.name,
				'roast' : { 'id' : coffee.roast.id, 'name' : str(coffee.roast), 'origin': coffee.roast.origin } if not variety_pack else None,
				'grinds' : self.serialize_grinds(coffee.grinds.all()),
				'sizes' : self.serialize_sizes(coffee.sizes.all(), coffee, check_featured, discount) if not variety_pack else None,
				'description' : coffee.description,
				'image_url' : coffee.image_url,
				'price_factor' : coffee.price_factor if not discount else coffee.price_factor - discount,
				'type' : 'coffee' if not coffee.wholesale else 'wholesale'
			}

			if check_featured:
				if coffee.featured is not None:

					obj['featured'] = {
							'id' : coffee.featured.id,
							'description': coffee.featured.description,
							'discount' : coffee.featured.discount, 
							'expiration_date' : coffee.featured.expiration_date,
						}
					if coffee.featured.display and obj['image_url']:
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


	def serialize_sizes(self, sizes, coffee, check_featured, discount):
		data = []

		customer_discount = discount if discount else 0

		if check_featured:
			featured_discount = 0 if coffee.featured is None else coffee.featured.discount
			featured_price_factor = (100 + float(coffee.price_factor) - featured_discount - customer_discount) / 100

		for size in sizes:
			obj = {
				'id' : size.id,
				'qty' : str(size),
				'ship_wt' : size.qty if size.unit == 'lbs' else float("{0:.2f}".format(size.qty / 16.0)),
				'base_price' : None if not check_featured else float("{0:.2f}".format(float(size.base_price) * featured_price_factor)),
				'base_price_plan' : float("{0:.2f}".format(float(size.base_price_plan) * ((100+coffee.price_factor-customer_discount)/100.0))),
			}



			data.append(obj)

		return data

	def serialize_subscriptions(self, subs, discount=None):
		data = []
		global db_modified

		for sub in subs:

			name = str(sub).split(' ')[:2]

			obj = {
				'id' : sub.id,
				'name' : ' '.join(name),
				'frequency' : sub.frequency,
				'coffees' : self.serialize_coffee(sub.coffees.all(), False, False, discount)[0],
				'image_url' : sub.image_url,
				'type' : 'subscription',
			}

			data.append(obj)

		db_modified = False

		return data


	def serialize_merch(self, products, check_featured=True):
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
				'type' : 'merchandise',
				'ship_wt' : float(merch.ship_wt)
			}

			if merch.featured is not None and check_featured:


				obj['featured'] = {
						'id' : merch.featured.id,
						'description': merch.featured.description,
						'discount' : merch.featured.discount, 
						'expiration_date' : merch.featured.expiration_date
					}

				obj['price'] *= (100-merch.featured.discount) / 100.0
				obj['price'] = float("{0:.2f}".format(obj['price']))


				if merch.featured.display and merch.image_url:
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
				'coffees' : self.serialize_coffee(pack.coffees.all(), False, True)[0],
				'merchandise' : self.serialize_merch(pack.merchandise.all(), False)[0],
				'price' : float(pack.price),
				'type' : 'variety',
				'ship_wt' : float(pack.ship_wt)

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

				if pack.featured.display and pack.image_url:
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

	def serialize_carousel(self, images):
		global db_modified
		data = []

		for slide in images:
			obj = {
				'id' : slide.id,
				'image_url' : slide.image_url,
				'image_alternate_text' : slide.image_alternate_text
			}
			data.append(obj)

		db_modified = False
		return data if len(data) > 0 else None

	def serialize_hours(self, hours):
		global db_modified
		data = []

		for day in hours:
			obj = {
				'id' : day.id,
				'monday_open' : day.monday_open,
				'monday_close' : day.monday_close,
				'tuesday_open' : day.tuesday_open,
				'tuesday_close' : day.tuesday_close,
				'wednesday_open' : day.wednesday_open,
				'wednesday_close' : day.wednesday_close,
				'thursday_open' : day.thursday_open,
				'thursday_close' : day.thursday_close,
				'friday_open' : day.friday_open,
				'friday_close' : day.friday_close,
			}
			if day.saturday_open and day.saturday_close:
				obj['saturday_open'] = day.saturday_open
				obj['saturday_close'] = day.saturday_close

			if day.sunday_open and day.sunday_close:
				obj['sunday_open'] = day.sunday_open
				obj['sunday_close'] = day.sunday_close

			data.append(obj)

		db_modified = False
		return data if len(data) > 0 else None

	def serialize_cafeContent(self, content):
		global db_modified
		data = []

		for cafe in content:
			obj = {
				'id' : cafe.id,
				'header' : cafe.header,
				'description' : cafe.description,
				'address' : cafe.address,
				'phone_number' : cafe.phone_number,
				'link_text' : cafe.link_text,
				'link_url' : cafe.link_url
			}
			data.append(obj)

		db_modified = False
		return data if len(data) > 0 else None

	def serialize_user(self, user):

		customer = None

		try:
			customer = Customer.objects.select_related('wholesale_price').prefetch_related('shippingaddress_set').get(user=user)
			obj = {
				'id' : user.id,
				'username' : user.username,
				'first_name' : user.first_name,
				'last_name' : user.last_name,
				'email' : user.email,
				'customer' : customer.id,
				'refreshOnLogin' : True if customer.wholesale_price.discount_rate else False,
				'shipping' : customer.shipping_address(False, True),
				'shipping_list' : [ address.shipping_address(False, True) for address in customer.shippingaddress_set.all()]
			}

		except Exception as e:
			obj = {
				'id' : user.id,
				'username' : user.username,
				'first_name' : user.first_name,
				'last_name' : user.last_name,
				'email' : user.email,
				'customer' : customer.id if customer else None
			}


		return obj


		
		

		
		
			