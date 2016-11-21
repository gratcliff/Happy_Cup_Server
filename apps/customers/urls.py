from django.conf.urls import url
from django.contrib.auth import views as auth_views
import views


urlpatterns = [

	url(r'^register/$', views.RegisterUser.as_view()),
	url(r'^edit/$', views.EditUser.as_view()),
	url(r'^user/$', views.GetCurrentUser.as_view()),
	url(r'^login/$', views.LoginUser.as_view()),
	url(r'^logout/$', views.logout_user),
	url(r'^password_change/$', auth_views.password_change, {'post_change_redirect':'/'}, name='password_change'),

]