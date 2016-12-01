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

		}
		self.shippingFee = 0
		self.totalItems = 0
		self.totalPrice = 0
		self.totalWeight = 0
		self.user = None

	def to_dictionary(self):

		return {
				"coffee" : self.coffee,
				"subscriptions" : self.subscriptions,
				"merch" : self.merch,
				"unsavedChanges" : self.unsavedChanges,
				"coupon" : self.coupon,
				"checkoutStatus" : self.checkoutStatus,
				"shippingFee" : self.shippingFee,
				"totalItems" : self.totalItems,
				"totalPrice": self.totalPrice,
				"totalWeight": self.totalWeight,
				"user" : self.user
			}

	def from_dictionary(self, data):

		self.coffee = data['coffee']
		self.subscriptions = data['subscriptions']
		self.merch = data['merch']
		self.unsavedChanges = data['unsavedChanges']
		self.coupon = data['coupon']
		self.checkoutStatus = data['checkoutStatus']
		self.shippingFee = data['shippingFee']
		self.totalItems = data['totalItems']
		self.totalPrice = data['totalPrice']
		self.totalWeight = data['totalWeight']
		self.user = data['user']


		return self

	def is_empty(self):
		return totalItems == 0



					


