happy_cup.controller('payment_controller', function ($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory){
	
	$scope.userAllowedInView = false;

	$scope.$emit('getShoppingCart', function(cart){
		if (cart.unsavedChanges || !cart.totalItems || !cart.checkoutStatus.payment) {
			$location.url('/cart');
		} else {
			$scope.currentCart = cart
			$scope.userAllowedInView = true;
		}
		


	});


});