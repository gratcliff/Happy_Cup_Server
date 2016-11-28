happy_cup.controller('profile_controller', function($scope, $location, user_factory){

	$scope.userAllowedInView = true;
	$scope.userEdit = false;
	$scope.profileEditForm = {};

	user_factory.getCurrentUser(function(currentUser){
		$scope.currentUser = currentUser;
		$scope.profileEditForm.prev_username = currentUser.username;
	});

	$scope.toggleForm = function(formType) {
		editMode($scope.currentUser);
		$scope.userEdit = true;	
	}

	$scope.cancelEdit = function() {
		$scope.userEdit = false;
	}

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
					console.log($scope.backendErrors);
					return
				}
			})
		// }
	}

	function editMode() {
		user_factory.getCurrentUser(function(currentUser){

			$scope.profileEditForm.username = currentUser.username;
			$scope.profileEditForm.first_name = currentUser.first_name;
			$scope.profileEditForm.last_name = currentUser.last_name;
			$scope.profileEditForm.email = currentUser.email;

		});
	}

});