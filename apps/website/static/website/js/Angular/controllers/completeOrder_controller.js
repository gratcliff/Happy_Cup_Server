happy_cup.controller('completeOrder_controller', function($scope, $location) {

	$scope.userAllowedInView = false;


	$scope.$emit('orderCompleted', function(orderCompleted){

		if (orderCompleted) {
			$scope.userAllowedInView = true;
		} else {
			$location.path('/')
		}

	});


});