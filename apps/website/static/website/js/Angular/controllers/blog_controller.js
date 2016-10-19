happy_cup.controller('blog_controller', function($scope, $http, $location, content_factory){

	$scope.posts = {};
	$scope.first_post = [];
	$scope.other_posts = [];
	$scope.blog_blocks = [];
	$scope.blog_block = [];
	$scope.limit = 1;
	$scope.loadMoreButton = true;
	$scope.count = 0;
	$scope.idx = 0;

	content_factory.getPageContent('blog', function(content){
			$scope.posts = content;
			$scope.first_post.push($scope.posts[0]);
			
			for(var x = 1; x < $scope.posts.length; x++){
				
				if(x % 3 == 0) {
					$scope.blog_block.push($scope.posts[x]);
					$scope.blog_blocks.push($scope.blog_block);
					$scope.blog_block = [];
					$scope.count = 0;
					$scope.idx += 1; 
					// if($scope.limit*3 == $scope.other_posts.length){
					// 	$scope.loadMoreButton = false;
					// }
				} else {
					$scope.blog_block.push($scope.posts[x]);
					$scope.blog_blocks[$scope.idx] = $scope.blog_block;
					$scope.count += 1;
				}
				$scope.other_posts.push($scope.posts[x]);
			};
	});
	console.log($scope.blog_blocks);

	$scope.loadMore = function() {
		$scope.limit += 3;
		if ($scope.limit >= $scope.other_posts.length - 1){
			$scope.loadMoreButton = false;
		}

		// $('html,body').animate({
		// 	scrollTop: $('.blogpost').offset().top
		// }, 500);
	};

});