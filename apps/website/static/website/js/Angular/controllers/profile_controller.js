happy_cup.controller('profile_controller', function($scope, $location, user_factory){

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
	}

	$scope.editMode = function(currentUser) {
		$scope.userEdit = true;
		$scope.backendErrors = undefined;	
		$scope.profileEditForm.username = currentUser.username;
		$scope.profileEditForm.first_name = currentUser.first_name;
		$scope.profileEditForm.last_name = currentUser.last_name;
		$scope.profileEditForm.email = currentUser.email;

	}

	$scope.removeSavedAddress = function(id) {
		user_factory.removeSavedAddress(id, function(currentUser) {
			$scope.$emit('userProfileChange', currentUser);
		});
	}

});