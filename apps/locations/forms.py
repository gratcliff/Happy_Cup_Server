from django import forms

from .models import Location
from .mapsapi import geocode_data

class LocationForm(forms.ModelForm):

	# number = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:85px'}))

	class Meta:
		model = Location
		fields = '__all__'

	def clean(self):

		cleaned_data = super(LocationForm, self).clean()

		data = geocode_data(cleaned_data)

		if data.get('error') is not None:
			self.add_error('address', data.get('message'))
		





