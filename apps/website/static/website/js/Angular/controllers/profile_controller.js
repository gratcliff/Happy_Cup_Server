happy_cup.controller('profile_controller', function($scope, $location, user_factory){

	$scope.userAllowedInView = true;
	$scope.userEdit = false;
	$scope.changePassword = false;

	user_factory.getCurrentUser(function(currentUser){
		$scope.currentUser = currentUser;
		console.log($scope.currentUser);
	});

	$scope.toggleForm = function(formType) {
		if(formType == $scope.currentUser.username){
			$scope.userEdit = true;	
		} else if(formType == $scope.currentUser.email){
			$scope.changePassword = true;
		}
	}

	$scope.cancelEdit = function() {
		$scope.userEdit = false;
		$scope.changePassword = false;
	}

});