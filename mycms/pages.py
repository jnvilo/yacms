import os

from  django.core.exceptions import ObjectDoesNotExist
from rest_framework import routers
from django.utils.text import slugify

from rest_framework import viewsets

from mycms import cmsfields
from . exceptions import NodeDoesNotExist
from . exceptions import PageDoesNotExist
from . utils import sanitize_path
from . models import Node
from . models import PageType
from . serializers import PageSerializerBase
from . registry import PageRegistry
from . cmsfields import CMSField


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
        
        """
        cls is a subclass of Page. We should iterate through all of the 
        members and filter the CMSField subclasses. 
        
        Each CMSField returns a serializer. 
        
        CMSField.get_serializer()
        
        class Meta:
            content = CMSContentField()
        
        content.get_serializer()
        
        """
        
        attribute_names = dir(cls) 
        attrs = {}
        
        for attribute_name in attribute_names:
            attribute = getattr(cls, attribute_name)
            if isinstance(attribute,(CMSField)):
                serializer = attribute.get_serializer()
                attrs.update({attribute_name: serializer })

        SerializerClass = type(name, (PageSerializerBase,), attrs )
        
        return SerializerClass
        #return PageSerializerBase
        
    @classmethod
    def build_viewset(cls):
        from .api import PageViewSet
        class_name = "{}ViewSet".format(cls.__name__)
        class_dict = { "serializer_class": cls.build_serializer()}
        ViewClass = type(class_name, (PageViewSet,),  class_dict )
        return ViewClass

        
from copy import deepcopy

class Page(BasePage): 
    
    node = cmsfields.CMSNodeField()
        
    def __init__(self, pk, *args, **kwargs): 
        
        self.pk = pk
     
 
    @property    
    def fields(self):
        """
        The field definitions are global instances that all classes have a
        reference to. 
        
        We want our own copy of the globaly defined fields. 
        
        """
        _fields = {}
        attribute_names = dir(self.__class__)
        for attribute_name in attribute_names:
            attribute = getattr(self.__class__, attribute_name)
            if isinstance(attribute,(CMSField)):
                attribute = deepcopy(attribute)
                _fields.update({attribute_name: attribute})
    
        return _fields         
        
            
    @property  
    def data(self):
        """
        Builds the data_dict for the page. Just iterates through the CMSFields
        and calls their get_values:
        """
        _data = {}
        
        for field_name, field_instance in self.fields.items():
            field_instance.initialize(self.pk)
            _data.update({field_name: field_instance.get_value()})
            
        return _data
        
        
        
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
        path = os.path.join(self._node.path, slug)
        
        node = Node()
        node.title = title
        node.path = path
        
        if not page_type(isinstance(obj, PageType)):
            pass
            
        node.page_type = page_type
        
        
    def render(self):
        
        from django.http import HttpResponse
        return HttpResponse("This is a test")
    
    def page_dict(self):
        
        pass
    
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