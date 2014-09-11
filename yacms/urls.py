
from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import sitemap
from . models import Pages

info_dict = { 
    
    'queryset': Pages.objects.all(),
    'date_field': 'date_modified',

}


sitemaps = {

    'cms' : GenericSitemap(info_dict, priority=0.9),

}

urlpatterns = [    
    
    
   url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    url(r'^(?P<path>[-/\.a-z\d_]*)$', 'yacms.views.page', name="page"),
]
