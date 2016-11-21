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
				content.global = {
				headerLogo : "https://dl.dropboxusercontent.com/u/8287719/resources/images/Banners/HC_Logo.png",
				};
				

			content.contact = {

			};
		

			
				callback(content);

			});

		
	}

	factory.getPageContent = function(page, callback) {

		var waitForContent = $interval(function(){
			if (content[page] !== undefined) {
				$interval.cancel(waitForContent);
				callback(content[page]);
			} 

		},10)

	}


	return factory;
});