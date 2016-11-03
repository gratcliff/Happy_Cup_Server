happy_cup.controller('checkout_controller', function ($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$emit('getShoppingCart', function(cart){
		if (cart.unsavedChanges || !cart.totalItems) {
			$location.url('/cart');
		} else {
			$scope.currentCart = cart
			$scope.userAllowedInView = true;
			$scope.forms.checkoutForm = {}
			$scope.billingInfo = {}
			$scope.shippingInfo = {}
			$scope.shippingInfo.sameAsBilling = true;
		}
		


	});

	$scope.submitBillingInfo = function() {
		$scope.forms.checkoutForm.$setSubmitted()
		if (!$scope.forms.checkoutForm.$valid) {
			$anchorScroll('billing-form-start');

	


		} else {
			if ($scope.shippingInfo.sameAsBilling) {
				$scope.shippingInfo = $scope.billingInfo;
				$scope.shippingInfo.sameAsBilling = true;
			}
			// shop_factory.submitBillingInfo($scope.billingInfo, $scope.shippingInfo, function(){
				// $location.url('/cart/payment');
			// });
		}
		
	};

});