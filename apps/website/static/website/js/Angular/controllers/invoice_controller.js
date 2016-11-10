happy_cup.controller('invoice_controller', function($scope, $location, shop_factory){

	$scope.userAllowedInView = false;

	$scope.$emit('viewInvoice', function(response){
		if (response.invoiceAvailable && response.order_id && response.customer_id) {

			shop_factory.getInvoice({order_id:response.order_id, customer_id:response.customer_id}, function(response){

				$scope.shipping = response.data.order.customer || response.data.charge.shipping;
				$scope.billing = response.data.charge.source
				$scope.order = response.data.order

				if ($scope.order.coffee) {
					$scope.order.coffee = JSON.parse($scope.order.coffee);
				}
				if ($scope.order.merch) {
					$scope.order.merch = JSON.parse($scope.order.merch);
				}
				if ($scope.order.subscriptions) {
					$scope.order.subscriptions = JSON.parse($scope.order.subscriptions);
				}

				$scope.userAllowedInView = true;

			});

		} else {
			$location.url('/')
		}

	});

});