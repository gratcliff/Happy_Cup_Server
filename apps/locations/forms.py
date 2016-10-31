from django.forms import ModelForm

from .models import Location
from .mapsapi import gmaps

class LocationForm(ModelForm):

	class Meta:
		model = Location
		fields = '__all__'

	def clean(self):

		cleaned_data = super(LocationForm, self).clean()

		try:
			data = gmaps.geocode(cleaned_data.get('address'))
			geometry = data[0].get('geometry')
			location = geometry.get('location')
			address =  data[0].get('formatted_address')
			(lat, lng) = (location.get('lat'), location.get('lng'))
			cleaned_data['lat'] = lat
			cleaned_data['lng'] = lng
			cleaned_data['address'] = address
		except Exception as e:
			if not data:
				self.add_error('address', 'Google Maps returned no results for this address.  Please double check for accuracy.')	
			else:
				self.add_error('address', 'Something went wrong. Please double check the address. Error message: '+str(e))
		





