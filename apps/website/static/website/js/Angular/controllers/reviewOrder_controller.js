happy_cup.controller('reviewOrder_controller', function($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$on('userLoggedOn', function(event, cart){
		$scope.currentCart = cart;
		$scope.currentCart.checkoutStatus.review = false
		$scope.currentCart.checkoutStatus.payment = false
		$location.url('/cart/checkout')
	});

	$scope.$emit('getShoppingCart', function(cart){

		if (!cart.checkoutStatus.review) {
			$location.url('/cart/payment');
		} else {
			$scope.userAllowedInView = true;
			$scope.currentCart = cart;
			console.log(cart);
		}

	});

	$scope.$on('completeOrder', function(event, data){		
		if (data.stripe) {
			$scope.stripe = data.stripe;
			$scope.billingInfo = data.billingInfo;
			console.log($scope.stripe)
		} else {
			$scope.userAllowedInView = false;
			$location.url('/cart/payment');
		}

	});


	$scope.submitOrder = function(){
		if (!$scope.submittingOrder) {

			$scope.submittingOrder = true;
			$scope.invalidBillingForm = undefined;
			var token = $scope.currentCart.subscriptions.length > 0 ? $scope.stripe : $scope.stripe.id 

			shop_factory.processPayment({token:token, email:$scope.billingInfo.email, phone_number:$scope.billingInfo.phone_number}, function(res) {
				if (res.data.error) {
					$scope.invalidBillingForm = res.data.error.message;
					$scope.submittingOrder = false;
					$anchorScroll('anchor-scroll');
				} else if (res.data.coupon_error) {
					$scope.invalidBillingForm = res.data.coupon_error;
					$scope.submittingOrder = false;
					$anchorScroll('anchor-scroll');
					$scope.currentCart.coupon.code = undefined;
					$scope.currentCart.coupon.valid = false;
					$scope.currentCart.coupon.discount = 0;
					shop_factory.updateCart($scope.currentCart, function(newCart){
						$scope.currentCart = newCart;
					});
					
				} else {

					if (res.data.order_id) {
						$scope.$emit('orderSubmitted', {order_id:res.data.order_id, customer_id:res.data.customer_id});
					} else {
						$scope.$emit('subscriptionSubmitted', {subscriptions:res.data.subscription_list, customer_id:res.data.customer_id});
					}

					
				}
				

			});

		}

	};



});