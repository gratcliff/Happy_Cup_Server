happy_cup.factory('content_factory', function($http, $interval){

	var factory = {};
	var content = {};


	factory.getContent = function(callback){

			$http.get('content/').then(function(response){
				content.home = response.data.home;
				// console.log(content.home.products);
				content.about = response.data.about;
				content.locations = response.data.locations;
				content.blog = response.data.blogPosts;
				content.cafe = response.data.cafe;
				content.stripe_public_key = response.data.stripe_public_key;
				content.contact = response.data.contact;
				content.global = {
				headerLogo : "https://s3-us-west-2.amazonaws.com/happycupwebsitefiles/resources/images/general_resources/HC_Logo.png",
				};
				
			
	
				callback(content);

			});

		
	};

	factory.getPageContent = function(page, callback) {

		var waitForContent = $interval(function(){
			if (content[page] !== undefined) {
				$interval.cancel(waitForContent);
				callback(content[page]);
			} 

		},10)

	};

	factory.openProductModal = function(product, type, callback) {

		angular.forEach(content.home.products[type], function(item, idx){
			if (item.id == product.id && item.name == product.name) {
				callback(item);
				return
			} else if (type == 'subscriptions') {

					if (item.id = product.subscription_id) {

						callback(item);
						return

					}
			}
			
		});

	};


	return factory;
});