happy_cup.controller('checkout_controller', function ($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$on('userLoggedOut', function(event, cart){
		$scope.currentCart = cart;
		$location.url('/')
	});

	$scope.$on('userLoggedOn', function(event, cart){
		$scope.currentCart = cart;
		$scope.populateForms(cart);
	});



	$scope.$emit('getShoppingCart', function(cart){
		if (cart.unsavedChanges || !cart.totalItems) {
			$location.url('/cart');
		} else {
			$scope.currentCart = cart
			$scope.userAllowedInView = true;
			$scope.shippingInfo = {};

			$scope.populateForms(cart);

		}
		


	});

	$scope.submitShippingInfo = function() {
		if (!$scope.submittingInfo) {
			$scope.submittingInfo = true;
			$scope.forms.checkoutForm.$setSubmitted()
			if (!$scope.forms.checkoutForm.$valid) {
				$anchorScroll('shipping-form-start');
				$scope.submittingInfo = false;
			} else {
				if ($scope.shippingInfo.saveShipping) {
					$scope.shippingInfo.user_id = $scope.currentCart.user.id;
					$scope.shippingInfo.customer_id = $scope.currentCart.user.customer;
				}

				shop_factory.submitShippingInfo($scope.shippingInfo, function(response){
					if (response.errors){

						for (field in response.errors) {
							$scope.forms.checkoutForm[field].$error.message = response.errors[field][0].message;
							$scope.forms.checkoutForm[field].$invalid = true;

						}
						$anchorScroll('Tel');
						$scope.submittingInfo = false;
					} else {
						$location.url('/cart/payment');
					}

			
				});
			}
		}
		
		
	};

	$scope.clearErrors = function(field){
		if ($scope.shippingInfo[field]) {

			$scope.forms.checkoutForm[field].$invalid = false;
			$scope.forms.checkoutForm[field].$error.message = undefined;

		}
	}

	$scope.populateForms = function(cart) {
		if (cart.shipping) {

			$scope.shippingInfo = cart.shipping

		} else if (cart.user) {

			if (cart.user.shipping) {
				var shipping = cart.user.shipping;

				$scope.shippingInfo = {
					first_name: cart.user.first_name,
					last_name: cart.user.last_name,
					phone_number: shipping.phone,
					email: shipping.email,
					address: shipping.address.line1,
					address2: shipping.address.line2,
					city: shipping.address.city,
					state: shipping.address.state,
					zipcode: shipping.address.postal_code,
					saveShipping: true
				};
			}
				
		}
	}

});