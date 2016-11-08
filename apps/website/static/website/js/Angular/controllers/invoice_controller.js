happy_cup.controller('invoice_controller', function($scope, $location, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$emit('viewInvoice', function(response){
		if (response.invoiceAvailable && response.order_id) {

			shop_factory.getInvoice(response.order_id, function(response){



				$scope.userAllowedInView = true;
			});


		} else {
			$location.url('/')
		}

	});

});