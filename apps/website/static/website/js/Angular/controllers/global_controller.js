happy_cup.controller('global_controller', function ($window, $scope, $location, $timeout, $interval, $anchorScroll, content_factory, user_factory, shop_factory){

	$scope.mobileAndTabletCheck = mobileAndTabletCheck();
	$scope.currentView = getCurrentView()
	$scope.pageTitle = 'Happy Cup Coffee Company - Portland, OR - Coffee Roasted by People with Potential'
	$scope.pageLoading = true;
	$scope.globalContent = {};
	$scope.forms = {};
	$scope.userReg = {};
	$scope.userLogin = {};
	$scope.authorizedUser = false;
	$scope.contact_marker = false;
	$scope.cartModalError = false;

	content_factory.getContent(function(content){
			$scope.globalContent = content.global;
			$scope.contactPage = content.contact;
			$scope.pageLoading = false;

			user_factory.getCurrentUser(function(currentUser){
				$scope.currentUser = currentUser

				shop_factory.getShoppingCart(function(cart){

					$scope.shoppingCart = cart;
					if ($scope.currentUser !== 'None') {
						$scope.shoppingCart.user = $scope.currentUser;
					}
				});

			});

	});

	$scope.registerUser = function() {

		$scope.backendErrors = undefined;

		if ($scope.forms.userRegForm.$valid) {
		
			user_factory.registerUser($scope.userReg, function(response){
				if (response.errors) {
					var errors = JSON.parse(response.errors);
					var errorList = []

					angular.forEach(errors, function(list, key){
						for (idx in list) {
							errorList.push(list[idx]);
						}
					});

					$scope.backendErrors = errorList

					return

				}
				//dismiss modal
				$timeout(function() {
					$scope.forms.userRegForm.$setUntouched();
					$scope.forms.userRegForm.$setPristine();
					$scope.userReg = {};
					$scope.dismissMobileModal();
					$('#user-reg-modal').modal('hide')
					$scope.userRegAlert = true;
					$scope.currentUser = response;
					$scope.shoppingCart.user = response;
					$scope.$broadcast('userLoggedOn', $scope.shoppingCart);
				}, 250);

				//dismiss flash alert
				$timeout(function() {
					$scope.userRegAlert = false;
				}, 2000);
				
			});

		}
		
	};

	$scope.loginUser = function() {
		if ($scope.userLogin.email_username && $scope.userLogin.password) {
			user_factory.loginUser($scope.userLogin, function(userData){
				if (userData.error) {
					$scope.userLogin.error = true;
				} else {
					
					//dismiss modal
					$timeout(function() {
						$scope.forms.userLoginForm.$setUntouched();
						$scope.forms.userLoginForm.$setPristine();
						$scope.userLogin = {};
						$scope.dismissMobileModal();
						$('#user-login-modal').modal('hide')
						$scope.userRegAlert = true;
						$scope.currentUser = userData;
						$scope.shoppingCart.user = userData;
						$scope.$broadcast('userLoggedOn', $scope.shoppingCart);
					}, 250);

					//dismiss flash alert
					$timeout(function() {
						if ($scope.currentUser.refreshOnLogin) {
							$window.location = '/';
						} else {
							$scope.userRegAlert = true;
						}
					}, 2000);
				}
			});
		} else {
			$scope.userLogin.error = true;
		}
	};

	$scope.resetForm = function(form, modelString, element) {
		// inputs are only reset when models are valid
		$scope[modelString] = {}
		form.$setUntouched();
		form.$setPristine();

		if (element) {
			$scope.dismissMobileModal();
		}
		
	}

	$scope.logout = function() {
		$scope.userLogoutAlert = 'Logging out...'
		user_factory.logout(function(response){
			$scope.currentUser = response;
				
			$timeout(function() {
				
				$scope.userLogoutAlert = 'You have successfully logged out.'
			}, 500);

			$timeout(function() {
				
				$window.location = '/'
			}, 1000);


		});
			
	}


	//event listeners

	$scope.$on('userProfileView', function(event, callback) {
		callback($scope.currentUser);
	});

	$scope.$on('userProfileChange', function(event, userData){
		user_factory.syncUser(userData, function(currentUser){
			$scope.currentUser = currentUser;
			$scope.shoppingCart.user = currentUser;
		});
	});

	$scope.$on('getShoppingCart', function (event, callback){
		var waitForContent = $interval(function(){
			if ($scope.shoppingCart !== undefined) {
				$interval.cancel(waitForContent);
				callback($scope.shoppingCart);
			}
		},10)
		
	});

	$scope.$on('openCoffeeModal', function (event, coffee, fromOrderHistory) {
		$scope.coffeeModal = coffee;
		$scope.coffeeOrder = {};
		$scope.coffeeOrder.size = coffee.sizes[0];
		$scope.coffeeOrder.grind = coffee.grinds[0];
		$scope.coffeeOrder.qty = 1
		$scope.cartModalError = false;
		if (fromOrderHistory) {
			$('#coffee_modal').modal('show');
		}
		$scope.mobileModal('#coffee_modal');

	
	});

	$scope.$on('openSubscriptionModal', function (event, sub, fromOrderHistory){

		$scope.subscriptionModal = sub;
		$scope.modalOrder = {};
		$scope.modalOrder.coffee = sub.coffees[0];
		$scope.modalOrder.grind = sub.coffees[0].grinds[0];
		$scope.modalOrder.size = sub.coffees[0].sizes[0]
		$scope.cartModalError = false;
		if (fromOrderHistory) {
			$('#subscription_modal').modal('show');
		}
		$scope.mobileModal('#subscription_modal');
		
	})

	$scope.$on('openMerchandiseModal', function (event, merch, fromOrderHistory){
		$scope.merchandiseModal = merch;
		$scope.modalOrder = {};
		$scope.cartModalError = false;

		if (merch.sizes) {
			$scope.modalOrder.size = merch.sizes[0];
		}

		if(merch.coffees){
			if (merch.coffee_qty > 1) {
				$scope.modalOrder.coffee = [];
				$scope.merchandiseModal.coffees = angular.copy(merch.coffees);
				// reset qty to 0 for each option
				angular.forEach($scope.merchandiseModal.coffees, function(coffee, key){
					coffee.qty = 0;

				});
			} else {
				$scope.modalOrder.coffee = merch.coffees[0];
				$scope.modalOrder.grind = merch.coffees[0].grinds[0];
			}
		}
		angular.forEach(merch.merchandise, function(item, idx){
			if (item.sizes) {
				$scope.modalOrder.size = item.sizes[0];
				$scope.merchandiseModal.sizes = item.sizes;
			}
		});
			
		if (fromOrderHistory) {
			$('#merch_modal').modal('show');
		}
		$scope.mobileModal('#merch_modal')
	})

	$scope.broadcastToCart = function(product, order, idx) {
		// disables button mashing
		if ($scope.addingProduct) {
			return
		}

		if (product.coffee_qty > 1) {

			if (order.coffee.length !== product.coffee_qty) {
				$scope.giftBoxError = true;
				return
			}

		}

		$scope.addingProduct = true;
		$scope.$broadcast('sendToCart', product, order, idx, function(response){
			$scope.cartModalError = true;
			$scope.addingProduct = false;
		});
		

	}

	// event listener eceived from shop_controller.addToCart()
	$scope.$on('addedToCart', function(event){
		$scope.addingProduct = false;
		$scope.dismissMobileModal()
	});

	// listens for route changes in order to style header appropriately
	$scope.$on("$routeChangeSuccess", function(event) {
		$scope.currentView = getCurrentView();
		$anchorScroll('page-top');
		$scope.pageTitle = 'Happy Cup Coffee Company - Portland, OR - Coffee Roasted by People with Potential'
	});

	$scope.$on('changePageTitle', function(event, title){
		$scope.pageTitle = title;
	});

	$scope.$on('contactController_designate', function (event){
		$scope.contact_marker = true;
	});

	$scope.$on('show_social', function (event){
		$scope.contact_marker = false;
	});

	$scope.$on('removeOldData', function(event){
		$scope.prevBillingInfo = undefined;
	});

	$scope.$on('reviewOrder', function(event, data){
		$scope.$apply(function(){
			$location.url('/cart/review');
			$scope.shoppingCart.checkoutStatus.review = true;
			$scope.prevBillingInfo = data.billingInfo
			$timeout(function(){
				$scope.$broadcast('completeOrder', data );
			},100);
			
		});
		
	});

	$scope.$on('orderSubmitted', function(event, data, fromOrderHistory){
		shop_factory.getShoppingCart(function(cart){
			$scope.shoppingCart = cart;
			$scope.orderCompleted = true;
			$scope.order_id = data.order_id;
			$scope.customer_id = data.customer_id;
			if ($scope.currentUser !== 'None') {
				$scope.shoppingCart.user = $scope.currentUser;
			}
			if (fromOrderHistory) {
				$scope.invoiceAvailable = true;
				$location.url('/cart/invoice');
			} else {
				$location.url('/cart/completed');
			}
			
		});
	})

	$scope.$on('subscriptionSubmitted', function(event, data, fromOrderHistory){
		shop_factory.getShoppingCart(function(cart){
			$scope.shoppingCart = cart;
			$scope.orderCompleted = true;
			$scope.subOrders = data.subscriptions;
			$scope.customer_id = data.customer_id;
			if ($scope.currentUser !== 'None') {
				$scope.shoppingCart.user = $scope.currentUser;
			}
			if (fromOrderHistory) {
				$scope.invoiceAvailable = true;
				$location.url('/cart/invoice');
			} else {
				$location.url('/cart/completed');
			}
		});
	})


	$scope.$on('orderCompleted', function(event, callback){
		callback($scope.orderCompleted);
		// user can only view page once per order submission
		$scope.orderCompleted = undefined;
		$scope.invoiceAvailable = true;
		
	});

	$scope.$on('sendEmailConfirmation', function(event){
		if ($scope.subOrders) {
			shop_factory.sendEmailConfirmation({subscriptions: $scope.subOrders, customer_id: $scope.customer_id}, function(response){
			});
		} else {
			shop_factory.sendEmailConfirmation({order_id: [$scope.order_id], customer_id: $scope.customer_id}, function(response){
			});
		}

	})



	$scope.$on('viewInvoice', function(event, callback){
		if ($scope.subOrders) {
			callback({invoiceAvailable:$scope.invoiceAvailable, subOrders:$scope.subOrders, customer_id:$scope.customer_id})
		} else {
			callback({invoiceAvailable:$scope.invoiceAvailable, order_id:$scope.order_id, customer_id:$scope.customer_id})
		}
		
		// user can only view page once per order submission
		$scope.invoiceAvailable = undefined;
		$scope.order_id = undefined;
		$scope.customer_id = undefined;
		$scope.subOrders = undefined;
	});

	// end of event listeners

	$scope.updateVarietyBox = function(choices, qtyLimit) {
		$scope.giftBoxError = false;

		var newChoices = [];
		var qtyAdded = 0;
		for (idx in choices) {
			qtyAdded = 0;
			if (choices[idx].qty > 0) {
				for (var i=0; i < choices[idx].qty; i++) {
					if (newChoices.length < qtyLimit) {
						newChoices.push(choices[idx]);
						qtyAdded++;
					} else {
						choices[idx].qty = qtyAdded;
						break;
					}
				}
			}
		}
		$scope.modalOrder.coffee = newChoices;
		if ($scope.modalOrder.coffee.length) {
			$scope.modalOrder.grind = newChoices[0].grinds[0];
		}


	}

	$scope.navbarCollapse = function() {
		var checkIfCollapsed = $('#btn-toggle-navbar').hasClass('collapsed');
		var mobileCheck = $('#btn-toggle-navbar').css('display') === 'block';

		// if menu is open and screen is mobile, collapse the menu
		if (!checkIfCollapsed && mobileCheck) {
			$('#btn-toggle-navbar').trigger('click');
		}

	}

	$scope.stopDefaultAction = function(element) {
		// prevents a dropdown menu from closing when clicked on
		
		try {
			$(element).off('click');
		} catch(err) {

		}
		
		$(element).click(function(e){
			e.stopPropagation();
		})
	}

	$scope.mobileModal = function(element) {	
		$scope.modalSelection = element;
	}

	$scope.dismissMobileModal = function() {	
		$scope.modalSelection = undefined;
		$scope.giftBoxError = false;
	}

	$scope.dismissModal = function(modal) {
		$(modal).modal('hide')
	}

	$scope.scrollToShop = function() {
		var waitForLoad = $interval(function(){
			try {
				$("body").animate({scrollTop: $('#product-tabs').offset().top-83}, "slow");
				$interval.cancel(waitForLoad);
			} catch (err) {

			}
		});
	}

	

	function getCurrentView(){
		// adds styling to navbar
		// reads current route, and returns the element between the first and second '/' in the route
		// if route is /cart/checkout, function returns 'cart'
		// if route is '', return 'home'
		
		var view = $location.path().split('/')[1]
		if (!view) {
			view = 'home'
		}
		return view
	}

	function mobileAndTabletCheck() {
		var check = false;
  	(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  	return check;
	}



});