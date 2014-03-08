from django.conf.urls import patterns, url
from budget import views

urlpatterns = patterns('',
		url(r'^$', views.login, name='login'),
		url(r'^$', views.index, name='index'),
		url(r'^login/$', views.login, name='login'),
		url(r'^logout/$', views.logout, name='logout'),
		url(r'^register/$', views.register, name='register'),
		url(r'^home/$', views.home, name='home'),
		url(r'^transactions/$', views.transactions, name='transactions'),
		url(r'^transactions/debit/$', views.debit, name='debit'),
		url(r'^transactions/credit/$', views.credit, name='credit'),
		url(r'^budget/$', views.budget, name='budget'),
		url(r'^categories/$', views.categories, name='categories'),
		url(r'^report/$', views.report, name='report'),
		url(r'^report/$', views.report, name='report'),
		url(r'^report/(?P<month>\d{2})/(?P<year>\d{4})/$', views.report, name='report'),
)
