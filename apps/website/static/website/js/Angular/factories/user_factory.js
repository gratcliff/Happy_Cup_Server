happy_cup.factory('user_factory',function($http){

	var factory = {};
	var currentUser = {};

	factory.getCurrentUser = function(callback){
			currentUser = 'None'
			callback(currentUser);
		
	};

	factory.registerUser = function(userData, callback){

		$http.post('customers/register/', userData).then(function(response){
			console.log(response)
			currentUser = userData
			callback(currentUser)
		});
		
	};

	factory.loginUser = function(userData, callback) {
		if (currentUser === 'None') {
			currentUser = {};
		}
		currentUser.username = userData.email_username;
		currentUser.first_name = 'Bob';
		callback(currentUser);
	};

	factory.logout = function(callback) {
		currentUser = 'None';
		callback(currentUser);
	};


	return factory;
});