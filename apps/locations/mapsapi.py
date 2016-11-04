import googlemaps
import os


try:
	gmaps = googlemaps.Client(os.environ.get('MAPSAPI_KEY'))
	gmaps_error = None
except Exception as e:
	gmaps_error = e



def geocode_data(cleaned_data):

	data = None

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
		if gmaps_error:
			return {'error': 'api', 'message': 'There is a problem with the Google Maps API.  Contact application support. Error : '+str(gmaps_error) }

		if not data:
			return {'error': 'no result', 'message': 'Google Maps returned no results for this address.  Please double check for accuracy.'	}
		else:
			return {'error': 'other', 'message': 'Something went wrong. Please double check the address or contact application support. Error message: '+str(e)}
		

def validate_address(final_address):

	data = None

	try:

		data = gmaps.geocode(final_address)
		comp = data[0].get('address_components')
		for key in comp:
			if 'street_number' in key['types']:
				number = key['short_name']
			elif 'route' in key['types']:
				street = key['short_name']
			elif 'locality' in key['types']:
				city = key['short_name']
			elif 'administrative_area_level_1' in key['types']:
				state = key['short_name']
			elif 'postal_code' in key['types']:
				zipcode = key['short_name']

		address_components = (number, street, city, state, zipcode)

		address = data[0].get('formatted_address')

		return (address, address_components)
	except Exception as e:
		# if gmaps_error:
		# 	return {'error': 'api', 'message': 'There is a problem with the Google Maps API.  Contact application support. Error : '+str(gmaps_error) }

		return ({'error': 'no result', 'message': 'Google Maps returned no results for this address.  Please double check your entry.'	},False)

		# 	return {'error': 'other', 'message': 'Something went wrong. Please double check the address. Error message: '+str(e)}		
