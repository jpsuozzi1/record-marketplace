"""myapp_microservices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from myapp import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/(?P<model>\w+)/create/$', views.create, name='create'),
    url(r'^api/v1/(?P<model>\w+)/(?P<model_id>\d+)/$', views.read, name='read'),
    url(r'^api/v1/(?P<model>\w+)/(?P<model_id>\d+)/update/$', views.update, name='update'),
    url(r'^api/v1/(?P<model>\w+)/(?P<model_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^api/v1/records/(?P<model_id>\d+)/all$', views.allSongsOnRecord, name='allSongsOnRecord'),
    url(r'^api/v1/allListings/$', views.allListings, name='allListings'),
    url(r'^api/v1/allRecords/$', views.allRecords, name='allRecords'),
    url(r'^api/v1/login/$', views.login, name='login'),
    url(r'^api/v1/logout/$', views.logout, name='logout')
]
