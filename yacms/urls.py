
from django.conf.urls import patterns, include, url
from yacms.views import  ( 
                       CMSContentsAPIView, 
                       CMSEntriesAPIView,
                       CMSMarkUpsAPIView,
                       CMSTemplatesAPIView,
                       CMSPageView,
                       CMSPathsAPIView,
                       CMSEntriesROAPIView,
                       LoremIpsumAPIView,
                       AssetsUploaderView,
                       CMSPageTypesAPIView, 
                       
                       )



urlpatterns = [    
    
    
   url(r'^api/v1/cmsentriesro', CMSEntriesROAPIView.as_view(), name="cmsentriesro_apiview"),
   

    #Read Write API Views
    url(r'^api/v1/cmspagetypes', CMSPageTypesAPIView.as_view(), name="cmspagetypes_apiview"),
    url(r'^api/v1/cmscontents/(?P<resource_id>[\d]+)/$', CMSContentsAPIView.as_view(), name="cmscontents_apiview"),
    url(r'^api/v1/cmscontents', CMSContentsAPIView.as_view(), name="cmscontents_apiview"),
    url(r'^api/v1/cmsentries/(?P<resource_id>[\d]+)/$', CMSEntriesAPIView.as_view(), name="cmsentries_apiview_detail"),
    url(r'^api/v1/cmsentries', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    url(r'^api/v1/cmsmarkups', CMSMarkUpsAPIView.as_view(), name="cmscmsmarkups_apiview"),
    url(r'^api/v1/cmstemplates', CMSTemplatesAPIView.as_view(), name="cmstemplates_apiview"),
        url(r'^api/v1/cmspaths', CMSPathsAPIView.as_view(), name="cmspaths_apiview"),
    url(r'^api/v1/cmspaths/(?P<resource_id>[\d]+)?/?$', CMSPathsAPIView.as_view(), name="cmspaths_apiview_detail"),
   
    url(r'^api/v1/loremipsum', LoremIpsumAPIView.as_view(), name="loremipsum"),
    
    #CMS API Custom Views
    url(r'^api/v1/cmsentries/(?P<id>[\d]*)/', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    url(r'^api/v1/cmsentries/(?P<slug>[-/\.a-z\d_]*)/', CMSEntriesAPIView.as_view(), name="cmsentries_apiview"),
    
    #Assets Manager Views
    url(r'^(?P<path>[-/\.a-z\d_]*)/assets_manager/(?P<filename>[-/\.a-z\d_]*)$', AssetsUploaderView.as_view(), name="assets_manager_post"),
    url(r'^(?P<path>[-/\.a-z\d_]*)/assets_manager/$', AssetsUploaderView.as_view(), name="assets_manager_get"),
    
    
    #CMS View - Returns website pages    
    url(r'^(?P<path>[-/\.a-z\d_]*)/$', CMSPageView.as_view(), name="cms_page"),
    url(r'^$', CMSPageView.as_view(), name="cms_page"),

    url(r'^fileupload$', 'yacms.views.fileupload', name="fileupload"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)/fileUploader/$', 'yacms.views.fileupload', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)/$', 'yacms.views.page', name="page"),
    #url(r'^(?P<path>[-/\.a-z\d_]*)$', 'yacms.views.page', name="page"),
   
]
