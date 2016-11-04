happy_cup.controller('checkout_controller', function ($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$emit('getShoppingCart', function(cart){
		if (cart.unsavedChanges || !cart.totalItems) {
			$location.url('/cart');
		} else {
			$scope.currentCart = cart
			$scope.userAllowedInView = true;
			$scope.forms.checkoutForm = {}
			$scope.shippingInfo = {}

			if (cart.shipping) {
				$scope.shippingInfo = cart.shipping
			}

		}
		


	});

	$scope.submitShippingInfo = function() {
		$scope.forms.checkoutForm.$setSubmitted()
		if (!$scope.forms.checkoutForm.$valid) {
			$anchorScroll('shipping-form-start');

		} else {
			shop_factory.submitShippingInfo($scope.shippingInfo, function(response){

				if (response.errors){

					for (field in response.errors) {
						$scope.forms.checkoutForm[field].$error.message = response.errors[field][0].message;
						$scope.forms.checkoutForm[field].$invalid = true;

					}
					$anchorScroll('Tel');
				} else {
					$location.url('/cart/payment');
				}

			
			});
		}
		
	};

	$scope.clearErrors = function(field){
		if ($scope.shippingInfo[field]) {

			$scope.forms.checkoutForm[field].$invalid = false;
			$scope.forms.checkoutForm[field].$error.message = undefined;

		}
	}

});