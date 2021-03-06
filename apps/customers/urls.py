from django.conf.urls import url
from django.contrib.auth import views as auth_views
import views


urlpatterns = [

	url(r'^register/$', views.RegisterUser.as_view()),
	url(r'^edit/$', views.EditUser.as_view()),
	url(r'^orders/$', views.GetOrderHistory.as_view()),
	url(r'^user/$', views.GetCurrentUser.as_view()),
	url(r'^login/$', views.LoginUser.as_view()),
	url(r'^logout/$', views.logout_user),
	url(r'^password_change/$', auth_views.password_change, name='password_change'),
	url(r'^password_change_done/$', auth_views.password_change_done, name='password_change_done'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
	url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
	url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

]