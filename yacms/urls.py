
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       
    url(r'^(?P<path>[-/\.a-z\d_]*)$', 'yacms.views.page', name="page"),
)
