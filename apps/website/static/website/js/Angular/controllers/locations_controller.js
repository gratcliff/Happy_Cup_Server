happy_cup.controller('locations_controller', function($scope, $http, $location, $timeout){

	$scope.expanded;
	$scope.mapLoaded = false;

	var radius = 10000;
	var map, myLatlng, myZoom, marker, radius_circle;
	var markers = [];
	// Set the coordinates of your location
	var options = {
                enableHighAccuracy: true,					
            };
    var infowindow = new google.maps.InfoWindow();

	navigator.geolocation.getCurrentPosition(function(position) {
		myLatlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
		myZoom = 12;
		initialize(myLatlng, myZoom);
		google.maps.event.addDomListener(window, "load", initialize);
		$scope.$apply(function(){
			$scope.mapLoaded = true;
		});
		
	},function(error) {
		alert('Unable to get location: ' + error.message);
	}, options);

	$timeout(function(){
		if (!$scope.mapLoaded) {
			$scope.mapLoadingError = true;
			$scope.mapLoaded = true;
		}
	}, 10000);
	
	var locations = [{
				name: 'Arbor Lodge',
				type: 'New Seasons Market',
				address: '6400 N Interstate Ave. Portland, OR 97217',
				number: 5034674777,
				url: 'https://www.newseasonsmarket.com/our-stores/arborlodge/',
				lat: 45.568861,
				lng: -122.681702
			},
			{
				name: 'Cedar Hills',
				type: 'New Seasons Market',
				address: '3495 SW Cedar Hills Blvd. Beaverton, OR 97005',
				number: 5036414181,
				url: 'https://www.newseasonsmarket.com/our-stores/cedarhills/',
				lat: 45.494353,
				lng: -122.812773
			},
			{
				name: 'Concordia',
				type: 'New Seasons Market',
				address: '5320 NE 33rd Ave. Portland, OR 97211',
				number: 5032883838,
				url: 'https://www.newseasonsmarket.com/our-stores/concordia/',
				lat: 45.561223, 
				lng: -122.630149
			},
			{
				name: 'Fisher\'s Landing',
				type: 'New Seasons Market',
				address: '2100B SE 164th Ave. Vancouver, WA 98683',
				number: 3607605005,
				url: 'https://www.newseasonsmarket.com/our-stores/fisherslanding/',
				lat: 45.605293, 
				lng: -122.506846
			},
			{
				name: 'Happy Valley',
				type: 'New Seasons Market',
				address: '15861 SE Happy Valley, Happy Valley, OR 97086',
				number: 5035589214,
				url: 'https://www.newseasonsmarket.com/our-stores/happyvalley/',
				lat: 45.428425, 
				lng: -122.499683
			},
			{
				name: 'Hawthorne',
				type: 'New Seasons Market',
				address: '4034 SE Hawthorne Blvd. Portland, OR 97214',
				number: 5032364800,
				url: 'https://www.newseasonsmarket.com/our-stores/hawthorne/',
				lat: 45.511822, 
				lng: -122.620710
			},
			{
				name: 'Mountain Park',
				type: 'New Seasons Market',
				address: '3 SW Monroe Parkway Lake Oswego, OR 97035',
				number: 5034961155,
				url: 'https://www.newseasonsmarket.com/our-stores/mountainpark/',
				lat: 45.433361, 
				lng: -122.703135
			},
			{
				name: 'Orenco Station',
				type: 'New Seasons Market',
				address: '1453 NE 61st Ave. Hillsboro, OR 97124',
				number: 5036486968,
				url: 'https://www.newseasonsmarket.com/our-stores/orencostation/',
				lat: 45.534287, 
				lng: -122.919214
			},
			{
				name: 'Progress Ridge',
				type: 'New Seasons Market',
				address: '14805 SW Barrows Road, Suite 103 Beaverton, OR 97007',
				number: 5035976777,
				url: 'https://www.newseasonsmarket.com/our-stores/progressridge/',
				lat: 45.430498, 
				lng: -122.829203
			},
			{
				name: 'Raleigh Hills',
				type: 'New Seasons Market',
				address: '7300 SW Beaverton Hillsdale Hwy. Portland, OR 97225',
				number: 5032926838,
				url: 'https://www.newseasonsmarket.com/our-stores/raleighhills/',
				lat: 45.485349, 
				lng: -122.752255
			},
			{
				name: 'Sellwood',
				type: 'New Seasons Market',
				address: '1214 SE Tacoma St. Portland, OR 97202',
				number: 5032304949,
				url: 'https://www.newseasonsmarket.com/our-stores/sellwood/',
				lat: 45.463969, 
				lng: -122.653635
			},
			{
				name: 'Seven Corners',
				type: 'New Seasons Market',
				address: '1954 SE Division St. Portland, OR',
				number: 5034452888,
				url: 'https://www.newseasonsmarket.com/our-stores/sevencorners/',
				lat: 45.504375, 
				lng: -122.646226
			},
			{
				name: 'Slabtown',
				type: 'New Seasons Market',
				address: '2170 NW Raleigh St, Portland, OR 97210',
				number: 5032247522,
				url: 'https://www.newseasonsmarket.com/our-stores/slabtown/',
				lat: 45.533763,
				lng: -122.696183
			},
			{
				name: 'Woodstock',
				type: 'New Seasons Market',
				address: '4500 SE Woodstock Blvd, Portland, OR 97206',
				number: 5037719663,
				url: 'https://www.newseasonsmarket.com/our-stores/woodstock/',
				lat: 45.479039, 
				lng: -122.616196
			},
			{
				name: 'Laurelhurst',
				type: 'Whole Foods Market',
				address: '2825 East Burnside St. Portland, Oregon',
				number: 5032326601,
				url: 'http://www.wholefoodsmarket.com/stores/laurelhurst',
				lat: 45.523260, 
				lng: -122.636734
			},
			{
				name: 'Pearl',
				type: 'Whole Foods Market',
				address: '1210 NW Couch St Portland, Oregon',
				number: 5035254343,
				url: 'http://www.wholefoodsmarket.com/stores/pearl',
				lat: 45.523471, 
				lng: -122.683358
			},
			{
				name: 'Hollywood',
				type: 'Whole Foods Market',
				address: '4301 NE Sandy Blvd Portland, Oregon',
				number: 5032842644,
				url: 'http://www.wholefoodsmarket.com/stores/sandy',
				lat: 45.536899, 
				lng: -122.618623
			},
			{
				name: 'Fremont',
				type: 'Whole Foods Market',
				address: '3535 NE 15th Ave. Portland, Oregon',
				number: 5032883414,
				url: 'http://www.wholefoodsmarket.com/stores/fremont',
				lat: 45.548822, 
				lng: -122.651160
			},
			{
				name: 'Bridgeport',
				type: 'Whole Foods Market',
				address: '7380 SW Bridgeport Rd. Tigard, Oregon',
				number: 5036396500,
				url: 'http://www.wholefoodsmarket.com/stores/tigard', 
				lat: 45.394410, 
				lng: -122.751549
			},
			{
				name: 'Mill Plain',
				type: 'Whole Foods Market',
				address: '815 Southeast 160th Avenue Vancouver, Washington',
				number: 3602534082,
				url: 'http://www.wholefoodsmarket.com/stores/millplain', 
				lat: 45.614694, 
				lng: -122.505816
			},
			{
				name: 'Greenway',
				type: 'Whole Foods Market',
				address: '12220 SW Scholls Ferry Rd, Tigard, OR 97223',
				number: 9713717000,
				url: 'http://www.wholefoodsmarket.com/stores/greenway',
				lat: 45.442458, 
				lng: -122.802794
			},
			{
				name: 'Belmont',
				type: 'Zupan\'s Markets',
				address: '3301 SE Belmont Portland, OR 97214',
				number: 5032393720,
				url: 'http://www.zupans.com/locations/store.php?l=belmont', 
				lat: 45.516681, 
				lng: -122.630659
			},
			{
				name: 'Burnside',
				type: 'Zupan\'s Markets',
				address: '2340 W Burnside Portland, OR 97210',
				number: 5034971088,
				url: 'http://www.zupans.com/locations/store.php?l=burnside',
				lat: 45.523103, 
				lng: -122.698743
			},
			{
				name: 'Lake Grove',
				type: 'Zupan\'s Markets',
				address: '16380 Boones Ferry Rd. Lake Oswego, OR 97035',
				number: 5032104190,
				url: 'http://www.zupans.com/locations/store.php?l=lake_grove',
				lat: 45.407022, 
				lng: -122.724269
			},
			{
				name: 'Macadam',
				type: 'Zupan\'s Markets',
				address: '7221 SW Macadam Ave. Portland, OR 97219',
				number: 5032445666,
				url: 'http://www.zupans.com/locations/store.php?l=macadam',
				lat: 45.472080, 
				lng: -122.671714
			},
			{
				name: 'Stadium',
				type: 'Fred Meyer',
				address: '100 NW 20th Portland, Oregon 97209',
				number: 5032732004,
				url: 'https://www.fredmeyer.com/storeHours?store=70100360',
				lat: 45.524159, 
				lng: -122.692815
			},
			{
				name: 'Hawthorne',
				type: 'Fred Meyer',
				address: '3805 SE Hawthorne Portland, Oregon 97214',
				number: 5038723300,
				url: 'https://www.fredmeyer.com/storeHours?store=70100135',
				lat: 45.512548, 
				lng: -122.623697
			},
			{
				name: 'Hollywood',
				type: 'Fred Meyer',
				address: '3030 NE Weidler Portland, Oregon 97232',
				number: 5032801300,
				url: 'https://www.fredmeyer.com/storeHours?store=70100600',
				lat: 45.532907,
				lng: -122.634873
			},
			{
				name: 'Glisan',
				type: 'Fred Meyer',
				address: '6615 NE Glisan St, Portland, OR 97213',
				number: 5037976940,
				url: 'https://www.fredmeyer.com/storeHours?store=70100125',
				lat: 45.527552, 
				lng: -122.595872
			},
			{
				name: 'Burlingame',
				type: 'Fred Meyer',
				address: '7555 SW Barbur Blvd, Portland, OR 97219',
				number: 5034523000,
				url: 'https://www.fredmeyer.com/storeHours?store=70100040',
				lat: 45.470554, 
				lng: -122.690408
			},
			{
				name: 'Raleigh Hills',
				type: 'Fred Meyer',
				address: '7700 SW Bvrtn Hillsdale Hwy, Portland, OR 97225',
				number: 5032920731,
				url: 'https://www.fredmeyer.com/storeHours?store=70100285',
				lat: 45.485414, 
				lng: -122.756057
			},
			{
				name: 'Otto\'s Sausage Kitchen',
				type: 'Markets & Co-ops',
				address: '4138 SE Woodstock Blvd. Portland, OR 97202',
				number: 5037716714,
				url: 'http://www.ottossausage.com/',
				lat: 45.478975, 
				lng: -122.619744
			},
			{
				name: 'Portland Fruit & Produce',
				type: 'Markets & Co-ops',
				address: '8040 SE Foster Rd. Portland, OR 97005',
				number: 5037770072,
				url: 'http://portlandfruitwest.com/pfp/',
				lat: 45.483238, 
				lng: -122.580510
			},
			{
				name: 'Portland Fruit West',
				type: 'Markets & Co-ops',
				address: '10205 SW Beaverton Hillsdale Hwy Beaverton, OR 97005',
				number: 5035743000,
				url: 'http://portlandfruitwest.com/',
				lat: 45.486617, 
				lng: -122.782219
			},
			{
				name: 'Food Fight!',
				type: 'Markets & Co-ops',
				address: '1217 SE Stark Portland, OR 97214',
				number: 5032333910,
				url: 'http://www.foodfightgrocery.com/',
				lat: 45.519498, 
				lng: -122.653269
			},
			{
				name: 'Food Front Co-op: Hillsdale',
				type: 'Markets & Co-ops',
				address: '6344 SW Capitol Highway, Hillsdale Shopping Center Portland, OR 97239',
				number: 5035466559,
				url: 'http://foodfront.coop/', 
				lat: 45.477926, 
				lng: -122.695583
			},
			{
				name: 'Food Front Co-op: Northwest',
				type: 'Markets & Co-ops',
				address: '2375 NW Thurman St. Portland, OR 97210',
				number: 5032225658,
				url: 'http://foodfront.coop/',
				lat: 45.535700, 
				lng: -122.700326
			},
			{
				name: 'Market of Choice: West Linn',
				type: 'Markets & Co-ops',
				address: '5639 Hood Street West Linn, OR 97068',
				number: 5035942901,
				url: 'http://www.marketofchoice.com/events/venue/west-linn',
				lat: 45.366683, 
				lng: -122.611755
			},
			{
				name: 'Neighbors Market',
				type: 'Markets & Co-ops',
				address: '1707 Main Street Vancouver, WA 98660',
				number: 3604486120,
				url: 'http://neighborsmarkets.com/', 
				lat: 45.634558, 
				lng: -122.671249
			},
			{
				name: 'Alberta St. Co-op',
				type: 'Markets & Co-ops',
				address: '1500 SE Alberta st. Portland, OR 97211',
				number: 5032874333,
				url: 'http://alberta.coop/', 
				lat: 45.558917,
				lng: -122.649515
			},
			{
				name: 'Beaumont Market',
				type: 'Markets & Co-ops',
				address: '4130 NE Fremont St. Portland, OR 97212',
				number: 5032843032,
				lat: 45.548134, 
				lng: -122.620118
			}, 
			{
				name: 'Chuck\’s Produce',
				type: 'Markets & Co-ops',
				address: '13215 SE Mill Plain Blvd Vancouver, WA 98684',
				number: 3605972700,
				url: 'http://chucksproduce.com/',
				lat: 45.618209, 
				lng: -122.536471
			},
			{
				name: 'Happy Cup Coffee Shop',
				type: 'Other',
				address: '446 NE Killingsworth Portland, Oregon',
				lat: 45.562440, 
				lng: -122.660544
			},
			{
				name: 'Delta Cafe',
				type: 'Other',
				address: '4607 SE Woodstock Portland, Oregon 97206',
				number: 5037713101,
				url: 'http://www.deltacafepdx.com/',
				lat: 45.479384,
				lng: -122.615186
			},
			{
				name: 'C Bar',
				type: 'Other',
				address: '2880 SE Gladstone St. Portland, Oregon 97202',
				number: 5032308808,
				url: 'http://cbarportland.com/',
				lat: 45.493205,
				lng: -122.635934
			}];


	$scope.locations = locations;
	var groupByStore = {}
	var markerColors = ['ltblue', 'orange', 'yellow', 'green', 'blue', 'pink', 'purple']

	angular.forEach($scope.locations, function(location, idx){
		if (!groupByStore[location.type]) {
			groupByStore[location.type] = '';
		}

	});

	var colorIdx = 0;

	for (key in groupByStore) {
		groupByStore[key] = markerColors[colorIdx % markerColors.length]

		colorIdx++;
	}

	$scope.storeGroup = groupByStore;

	$scope.updateMap = function(location){
		var myLatlng, myZoom, marker, markerColor;
		// Set the coordinates of your location
		myLatlng = new google.maps.LatLng(location.lat, location.lng);
		myZoom = 12;
		myDescription = location.address;
		myName = location.name;
		markerColor = 'https://maps.google.com/intl/en_us/mapfiles/ms/micons/'+groupByStore[location.type]+'-dot.png';
		setMarker(myLatlng, myDescription, myName, location.type, markerColor);
		google.maps.event.addDomListener(window, "load", initialize);

	};

	function initialize(myLatlng, myZoom) {
		var mapOptions = {
			zoom: myZoom,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			center: myLatlng,
			scrollwheel: false,
			styles: //style goes here 
			[
			    {
			        "featureType": "water",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "hue": "#e1e9eb"
			            },
			            {
			                "saturation": -48
			            },
			            {
			                "lightness": 18
			            }
			        ]
			    },
			    {
			        "featureType": "landscape.natural.terrain",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            },
			            {
			                "saturation": -5
			            }
			        ]
			    },
			    {
			        "featureType": "landscape.man_made",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "poi.school",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "poi.business",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "poi.park",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "poi.sports_complex",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "poi.attraction",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "poi.government",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "transit.line",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "road.arterial",
			        "elementType": "geometry",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "color": "#dedace"
			            }
			        ]
			    },
			    {
			        "featureType": "road.highway",
			        "elementType": "geometry",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "saturation": -21
			            },
			            {
			                "lightness": 48
			            }
			        ]
			    },
			    {
			        "featureType": "landscape.natural",
			        "elementType": "geometry.fill",
			        "stylers": [
			            {
			                "saturation": -13
			            },
			            {
			                "lightness": 47
			            }
			        ]
			    },
			    {
			        "featureType": "road.highway.controlled_access",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "transit.line",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "on"
			            }
			        ]
			    },
			    {
			        "featureType": "road",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "on"
			            }
			        ]
			    },
			    {
			        "featureType": "transit",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "administrative.neighborhood",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            },
			            {
			                "saturation": -52
			            },
			            {
			                "lightness": 61
			            }
			        ]
			    },
			    {
			        "featureType": "administrative.province",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "administrative.locality",
			        "elementType": "labels.text",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "saturation": -69
			            }
			        ]
			    },
			    {
			        "featureType": "poi",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "road.arterial",
			        "elementType": "geometry.fill",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "color": "#ffffff"
			            }
			        ]
			    },
			    {
			        "featureType": "transit.station",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "poi.park",
			        "elementType": "geometry",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "color": "#e9eee1"
			            }
			        ]
			    },
			    {
			        "featureType": "road.highway",
			        "elementType": "geometry",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "color": "#ffffff"
			            }
			        ]
			    },
			    {
			        "featureType": "road.local",
			        "elementType": "geometry.fill",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "color": "#fafafa"
			            },
			            {
			                "weight": 1
			            }
			        ]
			    },
			    {
			        "featureType": "road.local",
			        "elementType": "labels.icon",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "transit",
			        "elementType": "all",
			        "stylers": [
			            {
			                "visibility": "off"
			            }
			        ]
			    },
			    {
			        "featureType": "water",
			        "elementType": "geometry.fill",
			        "stylers": [
			            {
			                "visibility": "on"
			            },
			            {
			                "color": "#E1E9EB"
			            }
			        ]
			    }
			]						 
		};
		map = new google.maps.Map(document.getElementById("map-canvas"),mapOptions);
		marker = new google.maps.Marker({
			map:map,
			draggable:true,
			animation: google.maps.Animation.DROP,
			position: myLatlng
		});

		markers.push(marker);

		google.maps.event.addDomListener(window, "resize", function() {
			var center = marker.position;
			map.setCenter(center);
		});
		// markerInfo(map, marker);
		addYourLocationButton(map, marker);
		showCloseLocations(map, myLatlng);
	}

    function setMarker(position, description, name, type, color) {
        //Remove previous Markers.
        if (markers.length != null) {
            for (idx in markers) {
            	markers[idx].setMap(null);
            }
        }
        markers = [];
 
        //Set Marker on Map.
        marker = new google.maps.Marker({
            position: position,
            map: map,
            description: description,
            name: name,
            icon: color
        });
        markers.push(marker);
        map.setCenter(position);
 
        //Create and open InfoWindow.
        if(description){
	        var infoWindow = new google.maps.InfoWindow();
	        infoWindow.setContent('<p>'+type+' - '+name+'</p><p><a href = "https://maps.google.com/maps?q='+description+'" target="_blank">'+description+'</a></p>');
	        infoWindow.open(map, marker);	
        }

        marker.addListener('click', function(){
        	infoWindow.open(map, marker);
        });
    };

	function addYourLocationButton(map, marker) {
		var controlDiv = document.createElement('div');
		
		var firstChild = document.createElement('button');
		firstChild.style.backgroundColor = '#fff';
		firstChild.style.border = 'none';
		firstChild.style.outline = 'none';
		firstChild.style.width = '28px';
		firstChild.style.height = '28px';
		firstChild.style.borderRadius = '2px';
		firstChild.style.boxShadow = '0 1px 4px rgba(0,0,0,0.3)';
		firstChild.style.cursor = 'pointer';
		firstChild.style.marginRight = '10px';
		firstChild.style.padding = '0px';
		firstChild.title = 'Your Location';
		controlDiv.appendChild(firstChild);
		
		var secondChild = document.createElement('div');
		secondChild.style.margin = '5px';
		secondChild.style.width = '18px';
		secondChild.style.height = '18px';
		secondChild.style.backgroundImage = 'url(resources/images/mylocation-sprite-1x.png)';
		secondChild.style.backgroundSize = '180px 18px';
		secondChild.style.backgroundPosition = '0px 0px';
		secondChild.style.backgroundRepeat = 'no-repeat';
		secondChild.id = 'you_location_img';
		firstChild.appendChild(secondChild);
		
		google.maps.event.addListener(map, 'dragend', function() {
			$('#you_location_img').css('background-position', '0px 0px');
		});	

		firstChild.addEventListener('click', function() {
			setMarker(myLatlng);
			map.setCenter(myLatlng);
			$('#you_location_img').css('background-position', '-144px 0px');
		});
		
		controlDiv.index = 1;
		map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
	}

	function showCloseLocations(map, myLatlng) {
		radius_circle = new google.maps.Circle({
			center: myLatlng,
			radius: radius,
			clickable: false,
			map: map,
			fillOpacity: 0.1,
			strokeColor: '#F0EBD2',
            strokeOpacity: 0.8,
            strokeWeight: 2,
		});
		if(radius_circle) map.fitBounds(radius_circle.getBounds()); 
		for(x in locations) {
			var marker_lat_lng = new google.maps.LatLng(locations[x].lat, locations[x].lng);
			var distance_from_location = google.maps.geometry.spherical.computeDistanceBetween(myLatlng, marker_lat_lng);
			if (distance_from_location <= radius) {
				var markerColor = 'https://maps.google.com/intl/en_us/mapfiles/ms/micons/'+groupByStore[locations[x].type]+'-dot.png';
				markers.push(createMarker(marker_lat_lng, locations[x].address, locations[x].name, locations[x].type, markerColor));
  			}
		}	

	}

	function createMarker(pos, description, name, type, color) {
	    var marker = new google.maps.Marker({       
	        position: pos, 
	        map: map,
	        description: description,
	        name: name,
	        icon: color
	    }); 
	    google.maps.event.addListener(marker, 'click', function() { 
		    infowindow.setContent('<p>'+type+' - '+marker.name+'</p><p><a href = "https://maps.google.com/maps?q='+marker.description+'" target="_blank">'+marker.description+'</a></p>');
		    infowindow.open(map, marker);
	    }); 
	    return marker;  
	}

});