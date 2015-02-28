
from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import sitemap
from . views import CMSPageTypesAPIView
from . views import CMSContentsAPIView
from . views import CMSEntriesAPIView
from . views import CMSMarkUpsAPIView
from . views import CMSTemplatesAPIView

#info_dict = { 
    
    #'queryset': Pages.objects.all(),
    #'date_field': 'date_modified',

#}


#sitemaps = {

    #'cms' : GenericSitemap(info_dict, priority=0.9),

#}

urlpatterns = [    
    
    
   #url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
   #     name='django.contrib.sitemaps.views.sitemap'),

    #Basic API Views
    url(r'^api/v1/cmspagetypes', CMSPageTypesAPIView.as_view(), name="cmspagetypes_apiview"),
    url(r'^api/v1/cmscontents', CMSContentsAPIView.as_view(), name="cmscontents_apiview"),
    url(r'^api/v1/cmsentries', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    url(r'^api/v1/cmsmarkups', CMSMarkUpsAPIView.as_view(), name="cmscmsmarkups_apiview"),
    url(r'^api/v1/cmstemplates', CMSTemplatesAPIView.as_view(), name="cmstemplates_apiview"),
    
    
    #CMS API Custom Views
    url(r'^api/v1/cmsentries/(?P<id>[\d]*)/', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    url(r'^api/v1/cmsentries/(?P<slug>[-/\.a-z\d_]*)/', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    
    
    
    #url(r'^(?P<path>[-/\.a-z\d_]*)/mediauploader_endpoint/$', 'yacms.views.fileupload', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)/fileUploader/$', 'yacms.views.fileupload', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)/$', 'yacms.views.page', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)$', 'yacms.views.page', name="page"),
   
]
