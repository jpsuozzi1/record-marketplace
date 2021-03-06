"""myapp_web URL Configuration

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
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', views.home, name='home'),
    url(r'^listing/(?P<listing_id>\d+)/$', views.listing, name='listing'),
    url(r'^recordsList/$', views.recordsList, name='recordsList'),
    url(r'^createAccount/$', views.createAccount, name='createAccount'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^createListing/$', views.createListing, name='createListing'),
    url(r'^searchResults/$',views.searchResults, name='searchResults'),
    url(r'^$', RedirectView.as_view(url="/home/"), name='home'),
]
