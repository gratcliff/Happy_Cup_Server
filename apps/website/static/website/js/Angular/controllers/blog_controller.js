happy_cup.controller('blog_controller', function($scope, $http, $location, content_factory){

	$scope.posts = {};
	$scope.first_post = [];
	$scope.other_posts = [];

	content_factory.getPageContent('blog', function(content){
			$scope.posts = content;
			$scope.first_post.push($scope.posts[0]);
			for(var x = 1; x < $scope.posts.length; x++){
				$scope.other_posts.push($scope.posts[x]);
			};
	});

	$scope.backgrounds = [
		$scope.first_post[0].img_url, 
		$scope.other_posts[0].img_url,
		$scope.other_posts[1].img_url,
	]
	$scope.background = $scope.backgrounds[0];

	$('#carousel-blog-post').bind('slide.bs.carousel', function (e) {
		if($scope.background == $scope.backgrounds[0]) {
			$scope.background = $scope.backgrounds[1];
			$scope.$apply();
		} else if($scope.background == $scope.backgrounds[1]) {
			$scope.background = $scope.backgrounds[2];
			$scope.$apply();
		} else if($scope.background == $scope.backgrounds[2]) {
			$scope.background = $scope.backgrounds[0];
			$scope.$apply();
		}
	});

	// if($('#first_post').is(":visible")){
	// 	$('.parallax').css("background", "url('"+$scope.first_post[0].img_url+"') 50% 0px no-repeat");	
	// }

	// var x = document.getElementById($scope.other_posts[0].id);
	// var y = document.getElementById($scope.other_posts[1].id);
	// if($(x).is(":visible")){
	// 	$('.parallax').css("background", "url('"+$scope.other_posts[0].img_url+"') 50% 0px no-repeat");	
	// }

	// if($(y).is(":visible")){
	// 	$('.parallax').css("background", "url('"+$scope.other_posts[1].img_url+"') 50% 0px no-repeat");	
	// }

});