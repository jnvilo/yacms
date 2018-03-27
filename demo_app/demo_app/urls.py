"""demo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include


from django.conf.urls import url,include
from django.contrib import admin
from yacms.views import CMSFrontPage
from yacms.views import CMSLoginView
from yacms.views import CMSLogoutView
from yacms.views import CMSSitemap

from django.contrib.sitemaps.views import sitemap
from .views import TemplateSampleLoader

sitemaps = {
    'sitemaps': CMSSitemap,
}
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cms',include('yacms.urls')),
    url(r'^$', CMSFrontPage.as_view()),
    url(r'^login/', CMSLoginView.as_view()),
    url(r'^logout/', CMSLogoutView.as_view()),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^templates/(?P<template>[-._\w\d]*.html)$', TemplateSampleLoader.as_view()),
    url(r'^templates/?$', TemplateSampleLoader.as_view()),   
]