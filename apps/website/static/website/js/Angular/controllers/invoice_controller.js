happy_cup.controller('invoice_controller', function($scope, $location, shop_factory){

	$scope.userAllowedInView = false;


	$scope.$emit('viewInvoice', function(response){
		if (response.invoiceAvailable && response.order_id && response.customer_id) {

			shop_factory.getInvoice({order_id:response.order_id, customer_id:response.customer_id, order_type: response.order_type}, function(response){

				$scope.shipping = response.data.order.shipping_address || response.data.charge.shipping;
				$scope.billing = response.data.charge.source
				$scope.order = response.data.order

				if ($scope.order.coffee) {
					$scope.order.coffee = JSON.parse($scope.order.coffee);
				}
				if ($scope.order.merch) {
					$scope.order.merch = JSON.parse($scope.order.merch);
				}

				$scope.userAllowedInView = true;

			});

		} else if (response.invoiceAvailable && response.subOrders.length && response.customer_id){

			$scope.shipping = response.subOrders[0].order.shipping_address;
			$scope.billing = response.subOrders[0].billing[0];
			$scope.subscriptions = response.subOrders;
			$scope.totalPrice = 0;

			angular.forEach($scope.subscriptions, function(sub, idx){
				$scope.totalPrice += sub.order.totalPrice;
			});

			$scope.userAllowedInView = true;

		} else {
			$location.url('/')
		}

	});

});