happy_cup.controller('blogpost_controller', function($scope, $http, $location, $routeParams, content_factory){

	$scope.other_posts = [];
	$scope.post = [];

	content_factory.getPageContent('blog', function(content){
		for(x in content){
			if(content[x].id == $routeParams.id) {
				console.log(content[x]);
				$scope.post.push(content[x]);
			} else {
				$scope.other_posts.push(content[x]);
			}	
		}	
		$scope.$emit('changePageTitle', $scope.post[0].title);
	});

	$scope.fbShare = function(url, title, descr, image, winWidth, winHeight) {
        var winTop = (screen.height / 2) - (winHeight / 2);
        var winLeft = (screen.width / 2) - (winWidth / 2);
        window.open('http://www.facebook.com/sharer.php?s=100&p[title]=' + title + '&p[summary]=' + descr + '&p[url]=' + url + '&p[images][0]=' + image, 'sharer', 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
    }

    $scope.lkShare = function(url, title, descr, image, winWidth, winHeight) {
    	var winTop = (screen.height / 2) - (winHeight / 2);
        var winLeft = (screen.width / 2) - (winWidth / 2);
        window.open('http://www.linkedin.com/shareArticle?mini=true&url=' + url, 'sharer', 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
    }


});