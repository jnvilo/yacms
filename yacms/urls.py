from tastypie.api import Api

from django.conf.urls import patterns, include, url
from . api import PagesResource, PathsResource

v1_api = Api(api_name='v1')
v1_api.register(PagesResource())
v1_api.register(PathsResource())

urlpatterns = patterns('',
                       
    url(r'api/', include(v1_api.urls)),
    url(r'^(?P<path>[-/\.a-z\d_]*)$', 'yacms.views.page', name="page"),
)