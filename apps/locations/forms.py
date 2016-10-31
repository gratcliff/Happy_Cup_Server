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

		phone_number_length = len(str(cleaned_data.get('phone_number')))
		name_length = len(cleaned_data.get('name'))

		if data.get('error') == 'no result':
			self.add_error('address', data.get('message'))	
		elif data.get('error') == 'other':
			self.add_error('address', data.get('message'))
		
		if phone_number_length != 10:
			self.add_error('phone_number', 'Phone number must be 10 characters long.')

		if name_length < 3:
			self.add_error('name', 'Please enter a name.')





