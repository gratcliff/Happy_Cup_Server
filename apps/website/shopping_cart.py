from ..products.models import Coffee, Merchandise, Subscription, VarietyPack, ProductPromotion

from django.db import connection

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

class ShoppingCart(object):

	def __init__(self):
		self.coffee = []
		self.subscriptions = []
		self.merch = []
		self.unsavedChanges = False
		self.coupon = {'code' : None, 'valid': False, 'discount': 0 }
		self.checkoutStatus = {

			'payment' : False,
			'review' : False,
			'complete' : False

		}
		self.totalItems = 0
		self.totalPrice = 0

	def to_dictionary(self):

		return {
				"coffee" : self.coffee,
				"subscriptions" : self.subscriptions,
				"merch" : self.merch,
				"unsavedChanges" : self.unsavedChanges,
				"coupon" : self.coupon,
				"checkoutStatus" : self.checkoutStatus,
				"totalItems" : self.totalItems,
				"totalPrice": self.totalPrice
			}

	def from_dictionary(self, data):

		self.coffee = data['coffee']
		self.subscriptions = data['subscriptions']
		self.merch = data['merch']
		self.unsavedChanges = data['unsavedChanges']
		self.coupon = data['coupon']
		self.checkoutStatus = data['checkoutStatus']
		self.totalItems = data['totalItems']
		self.totalPrice = data['totalPrice']

		return self



def empty_all_carts():
	query = Session.objects.all()
	
	for session in query:
		decode = session.get_decoded()
		if decode.get('shoppingCart') is not None:
			data = SessionStore(session_key=session.session_key)
			data['shoppingCart'] = None
			data.save()

					


