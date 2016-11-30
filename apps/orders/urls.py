from django.conf.urls import url
import views

urlpatterns = [
	url(r'^coupon/$', views.VerifyCouponCode.as_view()),
	url(r'^address/$', views.CheckShippingAddress.as_view()),
	url(r'^payment/$', views.ProcessPayment.as_view()),
	url(r'^subscribe/$', views.ProcessSubscription.as_view()),
	url(r'^confirmation/$', views.SendEmailConfirmation.as_view()),
	url(r'^invoice/$', views.ProvideInvoice.as_view()),
	url(r'^cancel/$', views.CancelSubscription.as_view()),
	url(r'^webhooks/invoice/$', views.webhooks),

]