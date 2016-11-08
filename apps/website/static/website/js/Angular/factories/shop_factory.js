happy_cup.factory('shop_factory', function($http){

	var factory = {};
	var shoppingCart = {};

	//syncing or creating shoppingCart object

	
	
	
	//------- done creating shopping cart

	factory.getShoppingCart = function(callback) {

		$http.get('sync/').then(function(response){
			if (response.data.new) {

				shoppingCart.coffee = [];
				shoppingCart.subscriptions = [];
				shoppingCart.merch = [];
				shoppingCart.unsavedChanges = false;
				shoppingCart.coupon = {code: undefined, valid:false, discount: 0};
				shoppingCart.checkoutStatus = {
					payment : false,
					review : false,
				}


			} else {
				shoppingCart = response.data

			}

			shoppingCart.countTotals = function(){
				var totalItems = 0;
				var totalPrice = 0;
				for (idx in this.coffee) {
					totalItems += this.coffee[idx].qty;
					totalPrice += this.coffee[idx].subtotal;
				}
				for (idx in this.merch) {
					totalItems += this.merch[idx].qty;
					totalPrice += this.merch[idx].subtotal;
				}
				this.totalItems = totalItems;
				this.totalPrice = totalPrice;


			}
			shoppingCart.countTotals();
			callback(shoppingCart);

		});

		
	};

	factory.addCoffeeToCart = function(order, callback) {
		var identicalProduct = false;
		for (idx in shoppingCart.coffee) {
			// adjust the qty and price of the existing one

			if (shoppingCart.coffee[idx].id === order.id &&
			shoppingCart.coffee[idx].grind.id === order.grind.id &&
			shoppingCart.coffee[idx].size.id === order.size.id) {

				shoppingCart.coffee[idx].qty += order.qty;
				shoppingCart.coffee[idx].subtotal += order.subtotal;
				identicalProduct = true;
				break;
			}

		}
		if (!identicalProduct) {
			shoppingCart.coffee.push(order);
		}

		shoppingCart.totalItems += order.qty;
		shoppingCart.totalPrice += order.subtotal;

		$http.post('sync/', shoppingCart).then(function(response){
			callback(shoppingCart);
		});



		
	}		// if an identical product exists in the cart, 

	factory.addSubscriptionsToCart = function(order, callback) {
		var identicalProduct = false;
		for (idx in shoppingCart.subscriptions) {
			// adjust the qty and price of the existing one

			if (shoppingCart.subscriptions[idx].id === order.id &&
			shoppingCart.subscriptions[idx].grind.id === order.grind.id &&
			shoppingCart.subscriptions[idx].coffee.id === order.coffee.id) {

				shoppingCart.subscriptions[idx].qty += order.qty;
				shoppingCart.subscriptions[idx].subtotal += order.subtotal;
				identicalProduct = true;
				break;
			}

		}
		if (!identicalProduct) {
			shoppingCart.subscriptions.push(order);
		}

		shoppingCart.totalItems += order.qty;
		shoppingCart.totalPrice += order.subtotal;

		$http.post('sync/', shoppingCart).then(function(response){
			callback(shoppingCart);
		});
	}		

	factory.addMerchandiseToCart = function(order, callback) {

		var identicalProduct = false;
		for (idx in shoppingCart.merch) {

			for (key in order) {

				if (key == 'qty' || key == 'subtotal' || key == 'featured' || key == 'price') {
					continue;
				}
				if (!shoppingCart.merch[idx][key]) {
					identicalProduct = false;
					break;
				}

				if (typeof shoppingCart.merch[idx][key] == 'object') {

					if (shoppingCart.merch[idx][key].id === order[key].id) {
						continue;
					}

				}

				if (shoppingCart.merch[idx][key] != order[key]) {
					identicalProduct = false;
					break;
				}

				// loop did not break, so values are equal
				identicalProduct = true;


			}

			// only true if all key:values (excluding qty) are defined and equal
			if (identicalProduct) {
				shoppingCart.merch[idx].qty += order.qty;
				shoppingCart.merch[idx].subtotal += order.subtotal;
				identicalProduct = true;
				break;
			}

		}
		if (!identicalProduct) {
			shoppingCart.merch.push(order);
		}

		shoppingCart.totalItems += order.qty;
		shoppingCart.totalPrice += order.subtotal;



		$http.post('sync/', shoppingCart).then(function(response){
			callback(shoppingCart);
		});
	}			

	factory.updateCart = function(cart, callback){

		var nonZeroQtyCheck = [];
		for (idx in cart.coffee) {
			if (cart.coffee[idx].qty > 0) {
				nonZeroQtyCheck.push(cart.coffee[idx]);
			}
		}

		shoppingCart.coffee = nonZeroQtyCheck;
		nonZeroQtyCheck = [];
		for (idx in cart.subscriptions){
			if (cart.subscriptions[idx].qty > 0){
				nonZeroQtyCheck.push(cart.subscriptions[idx]);
			}
		}


		nonZeroQtyCheck = [];
		for (idx in cart.merch) {
			if (cart.merch[idx].qty > 0) {
				nonZeroQtyCheck.push(cart.merch[idx]);
			}
		}

		shoppingCart.merch = nonZeroQtyCheck;
		shoppingCart.countTotals();



		$http.post('sync/', shoppingCart).then(function(response){
			callback(shoppingCart);
		});
	};

	factory.removeProduct = function(idx, arrayName, callback) {
		shoppingCart[arrayName].splice(idx, 1);
		shoppingCart.countTotals();

		$http.post('sync/', shoppingCart).then(function(response){
			if (shoppingCart.totalItems === 0) {
				cart = response.data.shoppingCart
				delete shoppingCart.billing
				delete shoppingCart.shipping
				shoppingCart.checkoutStatus = cart.checkoutStatus
			}
			callback(shoppingCart);
		});

	}

	factory.submitCoupon = function(cart, callback) {
		var couponCode = cart.coupon.code;
		//post the coupon code to server and verify validity and discount

		var check = Math.random();
		if (check >= 0.5) {
			cart.coupon.valid = true;
			cart.coupon.discount = 0.15;
		}

		$http.post('sync/', shoppingCart).then(function(response){
			callback(shoppingCart);
		});
	};

	factory.submitShippingInfo = function (addressInfo, callback){
		$http.post('orders/address/', addressInfo).then(function(response){
			
			if (response.data.status === true) {
				shoppingCart.shipping = response.data.shoppingCart.shipping;
				shoppingCart.checkoutStatus.payment = true;
				callback(shoppingCart);
			} else {
				errors = JSON.parse(response.data.errors);
				callback({errors:errors});
			}
			
			

		});
	};

	factory.processPayment = function(token, callback) {
		$http.post('orders/payment/', token).then(function(response){
			callback(response)
		});
	};

	factory.getInvoice = function(id, callback){
		$http.get('orders/invoice/', id).then(function(response){
			callback(response);
		});
	}



	return factory;
});