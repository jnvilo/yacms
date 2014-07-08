from tastypie.resources import ModelResource
from yacms.models import Paths
from yacms.models import Pages


class PathsResource(ModelResource):
    class Meta:
        queryset = Paths.objects.all()
        resource_name = 'paths'
        
        
class PagesResource(ModelResource):
    class Meta:
        queryset = Pages.objects.all()
        resource_name = 'pages'