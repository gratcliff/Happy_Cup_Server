happy_cup.controller('order_controller', function ($scope, $location, $timeout, user_factory, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$emit('getShoppingCart', function(cart){
		if (cart.unsavedChanges || !cart.totalItems) {
			$location.url('/cart');
		} else {
			$scope.currentCart = cart
			$scope.userAllowedInView = true;
		}
		


	});



	$scope.orderComplete = function (){

	}
});