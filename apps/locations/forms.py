from django.forms import ModelForm

from .models import Location
from .mapsapi import geocode_data

class LocationForm(ModelForm):

	class Meta:
		model = Location
		fields = '__all__'

	def clean(self):

		cleaned_data = super(LocationForm, self).clean()

		data = geocode_data(cleaned_data)

		if data.get('error') == 'no result':
			self.add_error('address', data.get('message'))	
		elif data.get('error') == 'other':
			self.add_error('address', data.get('message'))
		





