from django.conf.urls import patterns, url
from budget import views

urlpatterns = patterns('',
		url(r'^$', views.home, name='home'),
		url(r'^login/$', views.login, name='login'),
		url(r'^register/$', views.register, name='register')
)
