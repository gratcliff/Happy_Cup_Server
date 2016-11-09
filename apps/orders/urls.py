from django.conf.urls import url
import views

urlpatterns = [
	url(r'^address/$', views.checkShippingAddress),
	url(r'^payment/$', views.ProcessPayment.as_view()),
	url(r'^invoice/$', views.ProvideInvoice.as_view()),

]