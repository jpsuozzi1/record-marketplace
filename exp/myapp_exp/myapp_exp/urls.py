"""myapp_exp URL Configuration

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
    url(r'^api/v1/recentListings/$', views.recentListings, name='recentListings'),
    url(r'^api/v1/listingDetails/(?P<model_id>\d+)/$', views.listingDetails, name='listingDetails'),
    url(r'^api/v1/recordsList/$', views.recordsList, name='recordsList'),
    url(r'^api/v1/login/$', views.login, name='login'),
    url(r'^api/v1/logout/$', views.logout, name='logout'),
    url(r'^api/v1/createAccount/$', views.createAccount, name='createAccount'),
    url(r'^api/v1/createListing/$', views.createListing, name='createListing'),
    url(r'^api/v1/search/$', views.search, name='search'),
]
