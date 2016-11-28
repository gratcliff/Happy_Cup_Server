happy_cup.controller('cafe_controller', function ($scope, $timeout, content_factory){

	content_factory.getPageContent('cafe', function(content){
		console.log(content);
		$scope.cafeContent = content.content;
		$scope.hours = content.hours;
		$scope.carousel = content.carousel;

		$timeout(function(){

			$('.cafe_slideshow').slick({
				accessibility: false,
				autoplay: true,
				autoplaySpeed: 5000,
				arrows: false,
				fade: true,
				mobileFirst: true,
				speed: 1000,
			});
		});

	});
		

});