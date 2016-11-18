from django.forms import ModelForm
from .models import ShippingFee

class ShippingFeeForm(ModelForm):

	class Meta:
		model = ShippingFee
		fields = '__all__'

	def clean(self):
		cleaned_data = super(ShippingFeeForm, self).clean()

		low = cleaned_data.get('min_weight')
		high = cleaned_data.get('max_weight')

		if low < 0:
			self.add_error('min_weight', 'Minimum weight cannot be less than 0')
			return
		if high < 0:
			self.add_error('max_weight', 'Maximum weight cannot be less than 0')
			return

		if high <= low:
			self.add_error('min_weight', 'Minimum weight cannot be greater than or equal to maximum')
			self.add_error('max_weight', 'Maximum weight cannot be less than or equal to minimum')
			return


		query = ShippingFee.objects.filter(min_weight__range=(low,high))

		if len(query):
			self.add_error('min_weight', 'Another shipping tier falls within this range')
			self.add_error('max_weight', 'Another shipping tier falls within this range')
			return

		query = ShippingFee.objects.filter(max_weight__range=(low,high))

		if len(query):
			self.add_error('min_weight', 'Another shipping tier falls within this range')
			self.add_error('max_weight', 'Another shipping tier falls within this range')
			return



