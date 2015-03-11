
from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import sitemap
from . views import  ( CMSPageTypesAPIView, 
                       CMSContentsAPIView, 
                       CMSEntriesAPIView,
                       CMSMarkUpsAPIView,
                       CMSTemplatesAPIView,
                       CMSPageView,
                       CMSPathsAPIView,
                       CMSEntriesROAPIView,
                       LoremIpsumAPIView,
                       )


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
   
   #Read Only List Views
   url(r'^api/v1/cmsentriesro', CMSEntriesROAPIView.as_view(), name="cmsentriesro_apiview"),
   

    #Read Write API Views
    url(r'^api/v1/cmspagetypes', CMSPageTypesAPIView.as_view(), name="cmspagetypes_apiview"),
    url(r'^api/v1/cmscontents', CMSContentsAPIView.as_view(), name="cmscontents_apiview"),
    url(r'^api/v1/cmsentries', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    url(r'^api/v1/cmsmarkups', CMSMarkUpsAPIView.as_view(), name="cmscmsmarkups_apiview"),
    url(r'^api/v1/cmstemplates', CMSTemplatesAPIView.as_view(), name="cmstemplates_apiview"),
    url(r'^api/v1/cmspaths', CMSPathsAPIView.as_view(), name="cmspaths_apiview"),
    url(r'^api/v1/loremipsum', LoremIpsumAPIView.as_view(), name="loremipsum"),
    
    
    #CMS API Custom Views
    url(r'^api/v1/cmsentries/(?P<id>[\d]*)/', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    url(r'^api/v1/cmsentries/(?P<slug>[-/\.a-z\d_]*)/', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    
    
    #CMS View - Returns website pages
    url(r'^(?P<path>[-/\.a-z\d_]*)/$', CMSPageView.as_view(), name="cms_page"),
    url(r'^$', CMSPageView.as_view(), name="cms_page")
   
    
    
    
    #url(r'^(?P<path>[-/\.a-z\d_]*)/mediauploader_endpoint/$', 'yacms.views.fileupload', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)/fileUploader/$', 'yacms.views.fileupload', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)/$', 'yacms.views.page', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)$', 'yacms.views.page', name="page"),
   
]
