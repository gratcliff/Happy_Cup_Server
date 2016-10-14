happy_cup.controller('about_controller', function ($scope, content_factory){

	content_factory.getPageContent('about', function(content){
		$scope.staff = content.staff
	});

});