happy_cup.controller('profile_controller', function($scope, $location, $timeout, user_factory, content_factory, shop_factory){

	$scope.$emit('userProfileView', function(currentUser) {
		if (currentUser === 'None') {
			$location.url('/');
		} else {
			
			$scope.userEdit = false;
			$scope.profileEditForm = {};

			user_factory.getOrderHistory(function(orders){
				$scope.orders = orders.orders;
				$scope.subscriptions = orders.subscriptions;
				$scope.userAllowedInView = true;
			});

			
		}
	});


	$scope.editUser = function(){

		$scope.backendErrors = undefined;
		// if($scope.profileEditForm.$valid){
			user_factory.editUser($scope.profileEditForm, function(response){
				if(response.errors) {
					var errors = JSON.parse(response.errors);
					var errorList = []

					angular.forEach(errors, function(list, key){
						for (idx in list) {
							errorList.push(list[idx]);
						}
					});
					$scope.backendErrors = errorList;
					return
				}
				$scope.userEdit = false;
				$scope.$emit('userProfileChange', response);

			})
		// }
	};

	$scope.editMode = function(currentUser) {
		$scope.userEdit = true;
		$scope.backendErrors = undefined;	
		$scope.profileEditForm.username = currentUser.username;
		$scope.profileEditForm.first_name = currentUser.first_name;
		$scope.profileEditForm.last_name = currentUser.last_name;
		$scope.profileEditForm.email = currentUser.email;

	};

	$scope.removeSavedAddress = function(id) {
		user_factory.removeSavedAddress(id, function(currentUser) {
			$scope.$emit('userProfileChange', currentUser);
		});
	};

	$scope.openCoffeeModal = function(id) {
		content_factory.openCoffeeModal(id, function(coffee){
			$scope.$emit('openCoffeeModal', coffee, true);
		});
	};

	$scope.$on('sendToCart', function(event, product, order, idx, callback) {
		var productType = product.type
		if (productType === 'coffee' || product.type === 'wholesale') {

			if ($scope.shoppingCart.subscriptions.length && typeof(callback) === 'function') {
				callback();
			} else {
				shop_factory.addCoffeeToCart(product, order, function(newCart){
					
					$timeout(function(){
						delete product.addingProduct
						$('#coffee_modal').modal('hide')
						// emits completion event to global controller
						$scope.$emit('addedToCart');
					}, 1000);

				});
			}

		} else if (productType === 'subscription'){

			if ($scope.shoppingCart.merch.length || $scope.shoppingCart.coffee.length) {

				if (typeof(callback) === 'function') {
					callback()
				} else {
					shop_factory.addSubscriptionsToCart(product, order, function(newCart){

						$timeout(function(){
							delete product.addingProduct
							$('#subscription_modal').modal('hide')
							// emits completion event to global controller
							$scope.$emit('addedToCart');
						}, 1000);

					});
				}


			}
			
		} else if (productType === 'merchandise' || productType === 'variety') {

			if ($scope.shoppingCart.subscriptions.length && typeof(callback) === 'function') {
				callback();
			} else {
				shop_factory.addMerchToCart(product, order, function(newCart){

					$timeout(function(){
						delete merch.addingProduct
						$('#merch_modal').modal('hide')
						$scope.$emit('addedToCart');
					}, 1000);
					
				});
			}
			
		}

	});

});