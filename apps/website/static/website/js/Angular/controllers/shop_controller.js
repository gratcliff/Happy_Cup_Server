happy_cup.controller('shop_controller', function ($scope, $timeout, content_factory, shop_factory){

	content_factory.getPageContent('home', function(content){
		$scope.products = content.products;
		
	});

// console.log($scope.products);

	$scope.productDisplay = {
		"showCoffee" : true,
		"showSubs" : false,
		"showMerch" : false
	};


	
	$scope.showCoffee = function (){
		$scope.productDisplay.showCoffee = true;
		$scope.productDisplay.showMerch = false;
		$scope.productDisplay.showSubs = false;
	}

	$scope.showSubs = function (){
		$scope.productDisplay.showCoffee = false;
		$scope.productDisplay.showMerch = false;
		$scope.productDisplay.showSubs = true;
	}

	$scope.showMerch = function (){
		$scope.productDisplay.showCoffee = false;
		$scope.productDisplay.showMerch = true;
		$scope.productDisplay.showSubs = false;
	}

	$scope.openCoffeeModal = function(coffee, idx) {
		coffee.idx = idx;
		$scope.$emit('openCoffeeModal', coffee);
		
	};
	$scope.openSubscriptionModal = function (sub, idx) {
		sub.idx =  idx;
		$scope.$emit('openSubscriptionModal', sub);
	}
	$scope.openMerchandiseModal = function (merch, idx) {
		merch.idx = idx;
		$scope.$emit('openMerchandiseModal', merch);
	}

	$scope.$on('sendToCart', function(event, product, order, idx) {
		// console.log(product.id);
		var productType = product.type.type
		if (productType === 'coffee') {
			$scope.addCoffeeToCart(product, order, idx);
		} else if (productType === 'subscription'){
			$scope.addSubscriptionsToCart(product, order, idx);
		} else if (productType === 'merchandise') {
			$scope.addMerchToCart(product, order, idx);
		}

	});

	$scope.addCoffeeToCart = function(coffee, order, idx) {
		$scope.products.coffee[idx].addingProduct = true;
		var data = {
			id: coffee.id,
			qty: 1,
			name: coffee.name,
			roast: coffee.roast,
			size: order.qty,
			grind: order.grind,
			subtotal: order.qty.price
		};
			
		shop_factory.addCoffeeToCart(data, function(newCart) {
			
			
			$timeout(function(){
				delete $scope.products.coffee[idx].addingProduct
				$('#coffee_modal').modal('hide')
				// emits completion event to global controller
				$scope.$emit('addedToCart');
			}, 1000);
		});

	}

	$scope.addSubscriptionsToCart = function(sub, order, idx){
		$scope.products.subscriptions[idx].addingProduct = true;
		var data = {
			id: sub.id,
			qty: 1,
			name: sub.name,
			roast: order.roast,
			grind: order.grind,
			price: sub.pricing,
			subtotal: sub.pricing
		};
		// console.log(data);
		shop_factory.addSubscriptionsToCart(data, function (newCart){

			$timeout(function(){
				delete $scope.products.subscriptions[idx].addingProduct
				$('#subscription_modal').modal('hide')
				$scope.$emit('addedToCart');
			}, 1000);
		});
	}

	$scope.addMerchToCart = function(merch, order, idx){
		$scope.products.merchandise[idx].addingProduct = true;
		var data = {
			id: merch.id,
			qty: 1,
			name: merch.name,
			price: merch.pricing,
			subtotal: merch.pricing
		};
		//Can be length 1 or 3
		if (order.roast){
			data.roast = order.roast;
		}
		if (order.grind){
			data.grind = order.grind;
		}
		if (order.size){
			data.size = order.size;
		}

		// console.log(data);
		shop_factory.addMerchandiseToCart(data, function (newCart){

			$timeout(function(){
				delete $scope.products.merchandise[idx].addingProduct
				$('#merch_modal').modal('hide')
				$scope.$emit('addedToCart');
			}, 1000);
		});
	}

	
})