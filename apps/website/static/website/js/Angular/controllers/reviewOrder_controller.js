happy_cup.controller('reviewOrder_controller', function($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$emit('getShoppingCart', function(cart){

		if (!cart.checkoutStatus.review) {
			$location.url('/cart/payment');
		} else {
			$scope.userAllowedInView = true;
			$scope.currentCart = cart;
		}

	});

	$scope.$on('completeOrder', function(event, data){		
		if (data.stripe) {
			$scope.stripe = data.stripe;
			$scope.billingInfo = data.billingInfo;
		} else {
			$scope.userAllowedInView = false;
			$location.url('/cart/payment');
		}

	});


	$scope.submitOrder = function(){
		if (!$scope.submittingOrder) {

			$scope.submittingOrder = true;
			$scope.invalidBillingForm = undefined;

			shop_factory.processPayment({token:$scope.stripe.id, email:$scope.billingInfo.email, phone_number:$scope.billingInfo.phone_number}, function(res) {
			
				if (res.data.error) {
					$scope.invalidBillingForm = res.data.error.message;
					$scope.submittingOrder = false;
					$anchorScroll('table-billing-info-start');
					return
				}

				$scope.$emit('orderSubmitted', res.data.order_id);

			});

		}

	};



});