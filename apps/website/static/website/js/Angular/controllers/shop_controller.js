happy_cup.controller('shop_controller', function ($scope, $timeout, content_factory, shop_factory){

	content_factory.getPageContent('home', function(content){
			$scope.products = content.products;
			if ($scope.products.featured) {
				$('#carousel-featured-products').carousel();
			}
			
	});

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
	$scope.openWholeSaleModal = function (coffee, idx){
		coffee.idx = idx;
		$scope.$emit('openWholeSaleModal', coffee);
	}
	$scope.openSubscriptionModal = function (sub, idx) {
		sub.idx =  idx;
		$scope.$emit('openSubscriptionModal', sub);
	}
	$scope.openMerchandiseModal = function (merch, idx) {
		merch.idx = idx;
		$scope.$emit('openMerchandiseModal', merch);
	}

	$scope.openFeaturedProductModal = function(product, mobileCheck) {

		if (product.type == 'coffee') {

			angular.forEach($scope.products.coffee, function(coffee, idx){
				if (product.id === coffee.id) {
					product.idx = idx;
					return
				}
			});

			emit_message = 'openCoffeeModal';
			modal = '#coffee_modal'
			console.log(product.idx, 'coffee');
		}
		else if (product.type == 'wholesale'){
			angular.forEach($scope.products.wholeSaleCoffee, function (coffee, idx){
				if (product.id === coffee.id){
					product.idx = idx;
					return
				}
			});

			emit_message = 'openWholeSaleModal';
			modal = '#wholesale_coffee_modal';
			console.log(product.idx, 'wholesale');
		}
		else if (product.type == 'merchandise' || product.type == 'variety') {

			angular.forEach($scope.products.merchandise, function(merch, idx){
				console.log(product);
				if (product.id === merch.id) {

					product.idx = idx;
					return
				}
			});
			emit_message = 'openMerchandiseModal';
			modal = '#merch_modal'
			console.log(product.idx, 'merch');

		}
		else if (product.type == 'subscription') {
			angular.forEach($scope.products.subscriptions, function(sub, idx){
				if (product.id === sub.id) {
					product.idx = idx;
					return
				}
			});
			emit_message = 'openSubscriptionModal';
			modal = '#subscription_modal'
		}

		$scope.$emit(emit_message, product)
		$(modal).modal('show')


	}

	$scope.$on('sendToCart', function(event, product, order, idx) {
		var productType = product.type
		if (productType === 'coffee') {
			$scope.addCoffeeToCart(product, order, idx);
		} else if (productType === 'subscription'){
			$scope.addSubscriptionsToCart(product, order, idx);
		} else if (productType === 'merchandise' || productType === 'variety') {
			$scope.addMerchToCart(product, order, idx);
		}

	});

	$scope.addCoffeeToCart = function(coffee, order, idx) {

		if (order.qty <= 0 || isNaN(order.qty)) {
			return
		}

		$scope.products.coffee[idx].addingProduct = true;
		var data = {
			id: coffee.id,
			name: coffee.name,
			roast: coffee.roast,
			featured: coffee.featured,
			size: order.size,
			grind: order.grind,
			qty: order.qty,
			subtotal: order.size.base_price * order.qty
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
			price: sub.price,
			subtotal: sub.price
		};

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
			price: merch.price,
			subtotal: merch.price,
			featured: merch.featured,

		};
		//Can be length 1 or 3
		if (order.coffee){
			data.coffee = order.coffee;
		}
		if (order.grind){
			data.grind = order.grind;
		}
		if (order.size){
			data.size = order.size;
		}


		shop_factory.addMerchandiseToCart(data, function (newCart){

			$timeout(function(){
				delete $scope.products.merchandise[idx].addingProduct
				$('#merch_modal').modal('hide')
				$scope.$emit('addedToCart');
			}, 1000);
		});
	}

	
})