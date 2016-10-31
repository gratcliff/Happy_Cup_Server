from django.conf.urls import url
import views

urlpatterns = [

	url(r'^$', views.Index.as_view()),
	url(r'^content/$', views.ProvideContent.as_view()),
	url(r'^sync/$', views.SyncShoppingCart.as_view())
	
]