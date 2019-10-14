import os

from  django.core.exceptions import ObjectDoesNotExist
from rest_framework import routers
from django.utils.text import slugify

from rest_framework import viewsets

from . exceptions import NodeDoesNotExist
from . exceptions import PageDoesNotExist
from . utils import sanitize_path
from . models import Node
from . models import PageType
from .serializers import PageSerializerBase


class PageRegistry(type):

    REGISTRY = {}
    VIEWCLASS_REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
       
        if cls.__name__ not in ["BasePage"]:
            cls.REGISTRY[new_cls.__name__] = new_cls
            return new_cls
        
    @classmethod 
    def sync_pagetypes_to_db(cls):
        """
        This makes sure that all the pages registered here 
        are also in the database. 
        """
        
        for name, klass in cls.REGISTRY.items():
            
            if name not in ["BasePage"]:
                cls._make_pagetype_db_entry(name, klass)
    
    @classmethod
    def _make_pagetype_db_entry(cls,name, klass):
        from mycms.models import PageType
        pt, c = PageType.objects.get_or_create( class_name = name)
        
        if c: 
            "It was just created, add the defaults"
            if klass.get_display_name():
                pt.display_name = klass.get_display_name()
            else:
                pt.display_name = klass.__name__
                
            if klass.get_base_path():
                pt.base_path = klass.get_base_path()
            else:
                pt.base_path = "/cms"
                
            if klass.get_template():
                pt.template = klass.get_template()

            pt.save()
                    
    @classmethod
    def register_api_views(self):
        pass
    
    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


    @classmethod
    def build_router_urls(cls, router):
        #router = routers.DefaultRouter()
        for name, klass in cls.REGISTRY.items():
            prefix = "api/v1/{}".format(name.lower())
            viewset = klass.build_viewset()
            router.register(prefix, viewset,basename=name.lower())
            
        return router.urls
    
class BasePage(metaclass=PageRegistry):
    
    @classmethod
    def get_name(cls):
        pass
    
    @classmethod
    def get_template(cls):
        pass

    @classmethod
    def get_display_name(cls):
        return getattr(cls.Meta, "name", None) if hasattr(cls, "Meta") else None
    
    @classmethod
    def get_base_path(cls):
        return getattr(cls.Meta, "base_path", None) if hasattr(cls, "Meta") else None

    @classmethod 
    def get_template(cls):
        return getattr(cls.Meta, "template", None) if hasattr(cls, "Meta") else None
    
    @classmethod
    def build_serializer(cls):
        """
        Builds a serializer for this class based on the CMSField definitions. 
        """
        name = "{}Serializer".format(cls.__name__) 
        SerializerClass = type(name, (PageSerializerBase,), {} )
        return SerializerClass
      
    @classmethod
    def build_viewset(cls):
        from .api import PageViewSet
        class_name = "{}ViewSet".format(cls.__name__)
        class_dict = { "serializer_class": cls.build_serializer()}
        ViewClass = type(class_name, (PageViewSet,),  class_dict )
        return ViewClass
        
        
        
class Page(BasePage): 
    
    #class Meta:
    #    name = "Page" #defaults to cls.__name__
    #    template = "base.html" #defaults to cls.__name__.html 
        
    def __init__(self, node, *args, **kwargs): 
        self.node = node
       
    @property 
    def name(self):
        pass
    
    @property 
    def template(self):
        pass
    
    @classmethod
    def load(cls, path):
        """
        creates a Page instance for the given path. Raises PageDoesNotExist 
        exception when the path could not be loaded. 
        """
        
        path = sanitize_path(path)
        try:
            node = Node.objects.get(path=path)
            instance = Page(node)
            return instance
        
        except ObjectDoesNotExist as e:    
            raise PageDoesNotExist("{} could not be found".format(path))
        
    
    def create_child(self, title, page_type, owner):
        
        slug = slugify(title)
        path = os.path.join(self.node.path, slug)
        
        node = Node()
        node.title = title
        node.path = path
        
        if not page_type(isinstance(obj, PageType)):
            pass
            
        node.page_type = page_type
        
        
    def render(self):
        
        from django.http import HttpResponse
        return HttpResponse("This is a test")
    
    
    
class PageData(object):
    """
    Encapsulates Page attributes that are to be sent
    to the template. 
    """
    
        
        
class TemplateAttributes(object):
    pass




class ViewSet(object):
    pass



class ArticlePage(Page):
    
    pass

class ListPage(Page):
    pass

class IndexPage(Page):
    pass