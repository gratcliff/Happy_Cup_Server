happy_cup.controller('completeOrder_controller', function($scope, $location) {

	$scope.userAllowedInView = false;

	$scope.$on('userLoggedOut', function(event, cart){
		$scope.currentCart = cart;
		$location.url('/')
	});

	$scope.$emit('orderCompleted', function(orderCompleted){

		if (orderCompleted) {
			$scope.userAllowedInView = true;

			$scope.$emit('sendEmailConfirmation');

		} else {
			$location.path('/')
		}

	});


});