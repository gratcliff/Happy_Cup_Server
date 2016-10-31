happy_cup.config(function($routeProvider, $interpolateProvider, $httpProvider){
	$interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

  

	$routeProvider
		.when('/',{
			templateUrl: staticURL+'website/partials/hc_index2.html',
		})
		.when('/about',{
			templateUrl: staticURL+'website/partials/hc_about_main.html',
		})
		.when('/blog',{
			templateUrl: staticURL+'website/partials/hc_blog_main.html',
		})
		.when('/blog/:id',{
			templateUrl: staticURL+'website/partials/hc_blog_post.html',
		})
		.when('/locations',{
			templateUrl: staticURL+'website/partials/hc_locations.html',
		})
		.when('/cafe',{
			templateUrl: staticURL+'website/partials/hc_cafe.html',
		})
		.when('/contact',{
			templateUrl: staticURL+'website/partials/hc_contact.html',
		})
		.when('/cart',{
			templateUrl: staticURL+'website/partials/hc_shop_cart.html',
		})
		.when('/cart/checkout',{
			templateUrl: staticURL+'website/partials/hc_shop_checkout.html',
		})
		.when('/cart/payment',{
			templateUrl: staticURL+'website/partials/hc_shop_checkout_payment.html',
		})
		.when('/cart/review',{
			templateUrl: staticURL+'website/partials/hc_shop_checkout_review.html',
		})
		.when('/cart/completed',{
			templateUrl: staticURL+'website/partials/hc_shop_checkout_completed.html',
		})
		.when('/cart/invoice',{
			templateUrl: staticURL+'website/partials/hc_shop_invoice.html',
		})
		.otherwise({
			templateUrl: staticURL+'website/partials/page-404.html'
		})
});


happy_cup.directive('moveToTop', function(){
	return {
		restrict: 'A',
		link: function(scope, $elm) {
			$elm.on('click', function(){
				$("body").scrollTop(0);
			});
		}
	}
});

happy_cup.directive('scrollToElement', function(){
	return {
		restrict: 'A',
		link: function(scope, $elm, attributes) {
			$elm.on('click', function(){
				$("body").animate({scrollTop: $(attributes.scrollToElement).offset().top}, "slow");
			});
		}
	}
});