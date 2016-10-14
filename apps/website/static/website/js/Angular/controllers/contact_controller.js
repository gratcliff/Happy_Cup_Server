happy_cup.controller('contact_controller', function ($scope, $location, content_factory){

	$scope.contact_marker = true;
	$scope.$emit('contactController_designate');

	$scope.$on("$destroy", function(){
        $scope.$emit('show_social');
    });

});