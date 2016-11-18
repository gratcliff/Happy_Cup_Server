happy_cup.controller('payment_controller', function ($scope, $location, $timeout, $anchorScroll, user_factory, shop_factory, content_factory){
	
	$scope.userAllowedInView = false;
	$scope.submittingPayment = false;

	$scope.$on('userLoggedOn', function(event, cart){
		$scope.currentCart = cart;
		$scope.currentCart.checkoutStatus.payment = false;
		$scope.currentCart.checkoutStatus.review = false;
	});


	$scope.$emit('getShoppingCart', function(cart){
		if (cart.unsavedChanges || !cart.totalItems || !cart.checkoutStatus.payment) {
			$location.url('/cart');
		} else {
			$scope.currentCart = cart;
			$scope.userAllowedInView = true;

			if ($scope.currentCart.sameAsBilling !== false) {
				$scope.currentCart.sameAsBilling = true		
				$scope.billingInfo = angular.copy($scope.currentCart.shipping)
			}
			
			$scope.paymentInfo = {}
			$scope.stripe = Stripe;

			content_factory.getPageContent('stripe_public_key', function(key){
				$scope.stripe.setPublishableKey(key);
			});

			

		}

	});

	$scope.toggleBillingInfo = function(){

		if ($scope.currentCart.sameAsBilling) {
			$scope.billingInfo = angular.copy($scope.currentCart.shipping)
		} else {
			$scope.billingInfo = {};
		}

		$scope.paymentInfo = {}

	}

	$scope.lookupCardType = function() {
		if ($scope.paymentInfo.number.length >= 12) {
			$scope.paymentInfo.cardType = $scope.stripe.card.cardType($scope.paymentInfo.number);
		} else {
			$scope.paymentInfo.cardType = undefined;
		}
	}

	$scope.submitPaymentInfo = function() {

		$scope.invalidBillingForm = undefined

		if (!$scope.currentCart.sameAsBilling) {

			$scope.forms.billingForm.$setSubmitted()

			if (!$scope.forms.billingForm.$valid) {
				$anchorScroll('shipping-info-check');
				return
			}

		}

		var validNumber = $scope.stripe.validateCardNumber($scope.paymentInfo.number);
		var validCvc = $scope.stripe.validateCVC($scope.paymentInfo.cvc);
		var validExp = $scope.stripe.validateExpiry($scope.paymentInfo.exp);

		if (validNumber && validCvc && validExp) {
			$scope.submittingPayment = true;

			var card_metadata = {'email':$scope.billingInfo.email, 'phone_number': $scope.billingInfo.phone_number};

			$scope.stripe.card.createToken({
				number: $scope.paymentInfo.number,
				cvc: $scope.paymentInfo.cvc,
				exp: $scope.paymentInfo.exp,
				name: $scope.billingInfo.first_name + " " + $scope.billingInfo.last_name,
				address_line1: $scope.billingInfo.address,
				address_line2: $scope.billingInfo.address2,
				address_city: $scope.billingInfo.city,
				address_state: $scope.billingInfo.state,
				address_zip: $scope.billingInfo.zipcode,
				
			}, $scope.stripeResponseHandler);
		} else {
			$scope.invalidBillingForm = 'Invalid credit card information';
			$anchorScroll('payment-form-start');
			$scope.submittingPayment = false;
		}

	}

	$scope.stripeResponseHandler = function(status, response) {
		if (response.error) {
			$scope.invalidBillingForm = response.error.message;
			$scope.submittingPayment = false;
			$scope.$apply()
			$anchorScroll('payment-form-start');
			return

		}
		$scope.$emit('reviewOrder', {'stripe' : response, billingInfo: $scope.billingInfo});


	}


});