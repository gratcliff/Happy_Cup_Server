happy_cup.controller('shop_controller', function ($scope, $timeout, $anchorScroll, content_factory, shop_factory){

	content_factory.getPageContent('home', function(content){
			$scope.products = content.products;
			if ($scope.products.featured) {
				$('#carousel-featured-products').carousel();
			}
			$scope.singleOrigins = []
			angular.forEach($scope.products.coffee, function(coffee, idx){

				if (coffee.roast.origin) {

					var origin = coffee.roast.origin;
					if ($scope.singleOrigins.indexOf(origin) == -1) {
						$scope.singleOrigins.push(origin);

					}

				}

				
			});
			$scope.singleOrigins.sort();
			
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

	$scope.openSubscriptionModal = function (sub, idx) {
		sub.idx =  idx;
		$scope.$emit('openSubscriptionModal', sub);
	};

	$scope.openMerchandiseModal = function (merch, idx) {
		merch.idx = idx;
		$scope.$emit('openMerchandiseModal', merch);
	};

	$scope.openFeaturedProductModal = function(product, mobileCheck) {

		if (product.type == 'coffee' || product.type == 'wholesale') {

			angular.forEach($scope.products.coffee, function(coffee, idx){
				if (product.id === coffee.id) {
					product.idx = idx;
					return
				}
			});

			emit_message = 'openCoffeeModal';
			modal = '#coffee_modal'
		}
		else if (product.type == 'merchandise' || product.type == 'variety') {

			angular.forEach($scope.products.merchandise, function(merch, idx){
				if (product.id === merch.id) {

					product.idx = idx;
					return
				}
			});
			emit_message = 'openMerchandiseModal';
			modal = '#merch_modal'

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

	$scope.$on('sendToCart', function(event, product, order, idx, callback) {
		var productType = product.type
		if (productType === 'coffee' || product.type === 'wholesale') {
			$scope.addCoffeeToCart(product, order, idx, callback);
		} else if (productType === 'subscription'){
			$scope.addSubscriptionsToCart(product, order, idx, callback);
		} else if (productType === 'merchandise' || productType === 'variety') {
			$scope.addMerchToCart(product, order, idx, callback);
		}

	});

	$scope.addCoffeeToCart = function(coffee, order, idx, callback) {
		if ($scope.shoppingCart.subscriptions.length) {
			$scope.cartError = true;
			$anchorScroll('product-tabs');
			if (typeof(callback) === 'function') {
				callback();
			}
			return
		}
		if (order.qty <= 0 || isNaN(order.qty)) {
			return
		}

		coffee.addingProduct = true;
		
			
		shop_factory.addCoffeeToCart(coffee, order, function(newCart) {
			
			
			$timeout(function(){
				delete coffee.addingProduct
				$('#coffee_modal').modal('hide')
				// emits completion event to global controller
				$scope.$emit('addedToCart');
			}, 1000);
		});

	}

	$scope.changeSubscriptionOptions = function(order, key) {
		var found = false;
			angular.forEach(order.coffee.sizes, function(size, idx){
				if (size.id == order.size.id) {
					order.size = size
					found = true;
				}
			});
			if (!found) {
				order.size = order.coffee.sizes[0];
			}

	}

	$scope.addSubscriptionsToCart = function(sub, order, idx, callback){
		if ($scope.shoppingCart.merch.length || $scope.shoppingCart.coffee.length) {
			$scope.cartError = true;
			$anchorScroll('product-tabs');
			console.log(typeof(callback))
			if (typeof(callback) === 'function') {
				callback();
			}
			return 
		}

		sub.addingProduct = true;

		shop_factory.addSubscriptionsToCart(sub, order, function (newCart){

			$timeout(function(){
				delete sub.addingProduct
				$('#subscription_modal').modal('hide')
				$scope.$emit('addedToCart');
			}, 1000);
		});
	}

	$scope.addMerchToCart = function(merch, order, idx, callback){
		if ($scope.shoppingCart.subscriptions.length) {
			$scope.cartError = true;
			$anchorScroll('product-tabs');
			if (typeof(callback) === 'function') {
				callback()
			}
			return
		}
		merch.addingProduct = true;


		shop_factory.addMerchandiseToCart(merch, order, function (newCart){

			$timeout(function(){
				delete merch.addingProduct
				$('#merch_modal').modal('hide')
				$scope.$emit('addedToCart');
			}, 1000);
		});
	}

	
});