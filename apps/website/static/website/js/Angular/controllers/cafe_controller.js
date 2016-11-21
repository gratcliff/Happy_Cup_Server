happy_cup.controller('cafe_controller', function ($scope, content_factory){

	content_factory.getPageContent('cafe', function(content){
		console.log(content);
		$scope.cafeContent = content.content;
		$scope.hours = content.hours;
		$scope.carousel = content.carousel;

	});
		

});