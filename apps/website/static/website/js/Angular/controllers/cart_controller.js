happy_cup.controller('cart_controller', function ($scope, $location, $timeout, user_factory, shop_factory){

	$scope.cartSaved = false;

	$scope.$on('userLoggedOut', function(event, cart){
		$scope.currentCart = cart;
		$location.url('/')
	});

	$scope.$on('userLoggedOn', function(event, cart){
		$scope.currentCart = cart;
	});


	$scope.$emit('getShoppingCart', function(cart){
			$scope.currentCart = cart;

			if (!$scope.currentCart.coupon.valid) {
				$scope.currentCart.coupon.code = undefined;
			}
	});
	

	$scope.updateCart = function() {
		$scope.cartSavedMessage = "Updating Shopping Cart..."
		shop_factory.updateCart($scope.currentCart, function(newCart){
			$scope.currentCart = newCart;
			$scope.currentCart.unsavedChanges = false;
			$scope.cartSavedMessage = 'Your cart has been updated';
			$timeout(function(){
				$scope.cartSavedMessage = false;
			}, 1500)
		});
	}

	$scope.removeProduct = function(idx, arrayName) {
		$scope.cartSavedMessage = "Updating Shopping Cart..."
		
		shop_factory.removeProduct(idx, arrayName,  function(newCart) {
			$scope.currentCart = newCart;
			$scope.currentCart.unsavedChanges = false;
			$scope.cartSavedMessage = 'Your cart has been updated';
			$timeout(function(){
				$scope.cartSavedMessage = false;
				if ($scope.currentCart.totalItems === 0){
					$location.path('/');
				}
			}, 1500);


			
		});

		
	};

	$scope.submitCoupon = function() {
		$scope.invalidCoupon = false;
		shop_factory.submitCoupon($scope.currentCart, function(newCart){
			if (!newCart.coupon.valid) {
				$scope.invalidCoupon = true;
			}
			$scope.currentCart = newCart;
		});
	};

	$scope.removeCoupon = function() {
		$scope.currentCart.coupon.code = undefined;
		$scope.currentCart.coupon.valid = false;
		$scope.currentCart.coupon.discount = 0;
		shop_factory.updateCart($scope.currentCart, function(newCart){
			$scope.currentCart = newCart;
		});
	}


});