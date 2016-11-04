happy_cup.controller('payment_controller', function ($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory){
	
	$scope.userAllowedInView = false;


	$scope.$emit('getShoppingCart', function(cart){
		if (cart.unsavedChanges || !cart.totalItems || !cart.checkoutStatus.payment) {
			$location.url('/cart');
		} else {
			$scope.currentCart = cart;
			$scope.userAllowedInView = true;
			$scope.currentCart.sameAsBilling = true;
			$scope.billingInfo = angular.copy($scope.currentCart.shipping)
			console.log($scope.currentCart)
		}

	});


	$scope.toggleBillingInfo = function(){

		if ($scope.currentCart.sameAsBilling) {
			$scope.billingInfo = angular.copy($scope.currentCart.shipping)
		} else {
			$scope.billingInfo = {}
		}

	}


});