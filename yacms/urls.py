
from django.conf.urls import patterns, include, url



urlpatterns = [                      
    url(r'^(?P<path>[-/\.a-z\d_]*)$', 'yacms.views.page', name="page"),
]
