happy_cup.factory('shop_factory', function($http){

	var factory = {};
	var shoppingCart = {};


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
				shoppingCart.shippingFee = 0;
				shoppingCart.user = undefined;


			} else {
				shoppingCart = response.data

			}

			shoppingCart.countTotals = function(){
				var totalItems = 0;
				var totalPrice = 0;
				var totalWeight = 0;
				for (idx in this.coffee) {
					totalItems += this.coffee[idx].qty;
					totalPrice = roundPrice(totalPrice,this.coffee[idx].subtotal);
					totalWeight += this.coffee[idx].ship_wt;
				}
				for (idx in this.merch) {
					totalItems += this.merch[idx].qty;
					totalPrice = roundPrice(totalPrice,this.merch[idx].subtotal);
					totalWeight += this.merch[idx].ship_wt;
				}
				for (idx in this.subscriptions) {
					totalItems += this.subscriptions[idx].qty;
					totalPrice = roundPrice(totalPrice,this.subscriptions[idx].subtotal);
					totalWeight += this.subscriptions[idx].ship_wt;
					console.log(totalWeight)
				}

				this.totalItems = totalItems;
				this.totalPrice = totalPrice;
				this.totalWeight = totalWeight;


			}
			shoppingCart.countTotals();
			callback(shoppingCart);

		});
		
	};

	factory.addCoffeeToCart = function(coffee, options, callback) {

		var order = {
			id: coffee.id,
			name: coffee.name,
			roast: coffee.roast,
			featured: coffee.featured,
			size: options.size,
			grind: options.grind,
			qty: options.qty,
			ship_wt: options.size.ship_wt * options.qty,
			subtotal: Math.round(options.size.base_price * 100 * options.qty) / 100
		};

		console.log(shoppingCart.coffee);


		var identicalProduct = false;
		for (idx in shoppingCart.coffee) {
			// if an identical product exists in the cart, 
			// adjust the qty and price of the existing one

			if (shoppingCart.coffee[idx].id === order.id &&
			shoppingCart.coffee[idx].grind.id === order.grind.id &&
			shoppingCart.coffee[idx].size.id === order.size.id) {

				shoppingCart.coffee[idx].qty += order.qty;
				shoppingCart.coffee[idx].subtotal += order.subtotal;
				shoppingCart.coffee[idx].ship_wt += order.ship_wt;
				identicalProduct = true;

				break;
			}

		}
		if (!identicalProduct) {
			shoppingCart.coffee.push(order);
		}

		shoppingCart.totalItems += order.qty;
		shoppingCart.totalPrice = roundPrice(shoppingCart.totalPrice, order.subtotal)
		shoppingCart.totalWeight += order.ship_wt;


		$http.post('sync/', shoppingCart).then(function(response){
			callback(shoppingCart);
		});
		
	}	

	factory.addSubscriptionsToCart = function(sub, options, callback) {

		var order = {
			id: sub.id,
			stripe_id : sub.stripe_id,
			qty: 1,
			name: sub.name,
			coffee: options.coffee,
			size: options.size,
			grind: options.grind,
			price: options.size.base_price_plan,
			subtotal: options.size.base_price_plan,
			shipments: options.shipments,
			ship_wt: options.size.ship_wt
		};



		var identicalProduct = false;
		for (idx in shoppingCart.subscriptions) {
			// adjust the qty and price of the existing one

			if (shoppingCart.subscriptions[idx].id === order.id &&
			shoppingCart.subscriptions[idx].grind.id === order.grind.id &&
			shoppingCart.subscriptions[idx].coffee.name === order.coffee.name &&
			shoppingCart.subscriptions[idx].size === order.size) {

				shoppingCart.subscriptions[idx].qty += order.qty;
				shoppingCart.subscriptions[idx].subtotal = roundPrice(shoppingCart.subscriptions[idx].subtotal,order.subtotal);
				shoppingCart.subscriptions[idx].ship_wt += order.ship_wt;
				identicalProduct = true;
				break;
			}

		}
		if (!identicalProduct) {
			shoppingCart.subscriptions.push(order);
		}

		shoppingCart.totalItems += order.qty;
		shoppingCart.totalPrice = roundPrice(shoppingCart.totalPrice,order.subtotal);
		shoppingCart.totalWeight += order.ship_wt;

		console.log(shoppingCart.totalWeight);		

		$http.post('sync/', shoppingCart).then(function(response){
			callback(shoppingCart);
		});
	}		

	factory.addMerchandiseToCart = function(merch, options, callback) {

		var order = {
			id: merch.id,
			qty: 1,
			name: merch.name,
			price: merch.price,
			subtotal: merch.price,
			featured: merch.featured,
			ship_wt: merch.ship_wt

		};
		//Can be length 1 or 3
		if (options.coffee){
			order.coffee = options.coffee;
		}
		if (options.grind){
			order.grind = options.grind;
		}
		if (options.size){
			order.size = options.size;
		}


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
				shoppingCart.merch[idx].subtotal = roundPrice(shoppingCart.merch[idx].subtotal,order.subtotal);
				shoppingCart.merch[idx].ship_wt = order.ship_wt;
				identicalProduct = true;
				break;
			}

		}
		if (!identicalProduct) {
			shoppingCart.merch.push(order);
		}

		shoppingCart.totalItems += order.qty;
		shoppingCart.totalPrice = roundPrice(shoppingCart.totalPrice,order.subtotal);
		shoppingCart.totalWeight += order.ship_wt;

		console.log(shoppingCart.totalWeight);		

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

		console.log(shoppingCart.totalWeight);		

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

				if (shoppingCart.billing) {
					shoppingCart.billing = {}
				}
				if (shoppingCart.shipping) {
					shoppingCart.shipping = {}
				}

				shoppingCart.checkoutStatus = cart.checkoutStatus
			}
			callback(shoppingCart);
		});

	}

	factory.submitCoupon = function(cart, callback) {
		var couponCode = cart.coupon.code;
		//post the coupon code to server and verify validity and discount
		$http.post('orders/coupon/', couponCode).then(function(response){
			console.log(response.data);
			var coupon = response.data;
			if (coupon.valid) {
				shoppingCart.coupon = coupon;
			}
			callback(shoppingCart)

		});
	};

	factory.submitShippingInfo = function (addressInfo, callback){
		$http.post('orders/address/', addressInfo).then(function(response){
			
			if (response.data.status === true) {
				shoppingCart.shipping = response.data.shoppingCart.shipping;
				shoppingCart.shippingFee = response.data.shoppingCart.shippingFee
				shoppingCart.subscriptions = response.data.shoppingCart.subscriptions
				shoppingCart.checkoutStatus.payment = true;
				shoppingCart.user = response.data.shoppingCart.user;
				callback(response);
			} else {
				errors = JSON.parse(response.data.errors);
				callback({errors:errors});
			}
			
			

		});
	};

	factory.processPayment = function(token, callback) {
		if (!shoppingCart.subscriptions.length) {
			$http.post('orders/payment/', token).then(function(response){
				callback(response);
			});
		} else {
			$http.post('orders/subscribe/', token).then(function(response){
				callback(response);
			});
		}
	};

	factory.sendEmailConfirmation = function(data, callback) {
		if (data.subscriptions) {
			data.order_id = [];
			angular.forEach(data.subscriptions, function(sub, idx){
				data.order_id.push(sub.order.id);
			});
		}
		$http.post('orders/confirmation/', data).then(function(response){
			callback()
		});
	}

	factory.getInvoice = function(data, callback){
		$http.post('orders/invoice/', data).then(function(response){
			callback(response);
		});
	}

	function roundPrice(previous, additional) {


		previous *= 100;
		additional *= 100;
		previous = Math.round(previous)
		additional = Math.round(additional)

		return (previous + additional) / 100;

	}

	return factory;
});