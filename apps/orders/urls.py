from django.conf.urls import url
import views

urlpatterns = [
	url(r'^coupon/$', views.VerifyCouponCode.as_view()),
	url(r'^address/$', views.checkShippingAddress),
	url(r'^payment/$', views.ProcessPayment.as_view()),
	url(r'^confirmation/$', views.SendEmailConfirmation.as_view()),
	url(r'^invoice/$', views.ProvideInvoice.as_view()),

]