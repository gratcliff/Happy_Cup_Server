import googlemaps
import os

gmaps = googlemaps.Client(os.environ.get('MAPSAPI_KEY'))


def geocode_data(cleaned_data):

	try:
			data = gmaps.geocode(cleaned_data.get('address'))
			geometry = data[0].get('geometry')
			location = geometry.get('location')
			address =  data[0].get('formatted_address')
			(lat, lng) = (location.get('lat'), location.get('lng'))
			cleaned_data['lat'] = lat
			cleaned_data['lng'] = lng
			cleaned_data['address'] = address
			return cleaned_data
	except Exception as e:
		if not data:
			return {'error': 'no result', 'message': 'Google Maps returned no results for this address.  Please double check for accuracy.'	}
		else:
			return {'error': 'other', 'message': 'Something went wrong. Please double check the address. Error message: '+str(e)}
		


