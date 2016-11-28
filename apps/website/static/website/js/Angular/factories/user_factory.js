happy_cup.factory('user_factory',function($http){

	var factory = {};
	var currentUser = {};

	factory.getCurrentUser = function(callback){

			$http.get('customers/user').then(function(response){
				if (response.data.status) {
					currentUser = response.data.user;
				} else {
					currentUser = 'None'
				}
				callback(currentUser);
			});
	};

	factory.registerUser = function(userData, callback){

		$http.post('customers/register/', userData).then(function(response){
			if (response.data.errors) {
				callback(response.data);
			} else {
				currentUser = response.data.user
				callback(response.data.user);
			}
			
			
		});
		
	};

	factory.editUser = function(userData, callback){
		console.log(userData);
		$http.post('customers/edit/',userData).then(function(response){
			if (response.data.errors) {
				callback(response.data);
			} else {
				currentUser = response.data.user
				callback(response.data.user);
			}

		});
	}

	factory.loginUser = function(userData, callback) {
		if (currentUser === 'None') {
			currentUser = {};
		}
		$http.post('customers/login/', userData).then(function(response){
			if (response.data.status) {
				currentUser = response.data.user;
				callback(currentUser);
			} else {
				currentUser = 'None';
				callback({error:true});
			}
		});

	};

	factory.logout = function(callback) {
		$http.get('customers/logout/').then(function(response){
			currentUser = 'None';
			callback(currentUser);
		});
	};


	return factory;
});