from django import forms

from .models import Location
from .mapsapi import geocode_data

class LocationForm(forms.ModelForm):

	class Meta:
		model = Location
		fields = '__all__'

	def clean(self):

		cleaned_data = super(LocationForm, self).clean()

		phone_number_length = len(str(cleaned_data.get('phone_number')))
		name_length = len(cleaned_data.get('name'))

		data = geocode_data(cleaned_data)


		if data.get('error') is not None:
			self.add_error('address', data.get('message'))

		if phone_number_length != 10:
			self.add_error('phone_number', 'Phone number must be 10 characters long.')

		if name_length < 3:
			self.add_error('name', 'Please enter a valid name. 3 characters minimum.')





