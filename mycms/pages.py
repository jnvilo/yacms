import os
from functools import lru_cache

from  django.core.exceptions import ObjectDoesNotExist
from rest_framework import routers
from django.utils.text import slugify
from django.http import response

from rest_framework import viewsets

from mycms import cmsfields
from . exceptions import NodeDoesNotExist
from . exceptions import PageDoesNotExist
from mycms import exceptions as cmsexceptions
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
        Builds the root serializer for this class based on the 
        CMSField definitions. 
        """
        name = "{}Serializer".format(cls.__name__)     
        attribute_names = dir(cls) 
        attrs = {}
        
        """
        All Page subclassses would have one or more field defnitions 
        at the top of the page. (Does not have to be at the top).
        
        class CustomPage(Page):
        
            content = cmsfields.CMSContentField()
            node = cmsfields.CMSNodeField()
        
        We iterate through the class attributes and filter out anything that is
        subclass of a CMSField and get its serializer class which then 
        gets added as an instance attribute. 
        """
        
        for attribute_name in attribute_names:
            attribute = getattr(cls, attribute_name)
            if isinstance(attribute,(CMSField)):
                serializer = attribute.get_serializer()
                
                """
                Now add an instance of the serializer for the field. 
                Note that this could also just be a serializer.Field attribute. 
                """
                
                attrs.update({attribute_name: serializer() })

       
        print(attrs)
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
        self._fields =  None
        
    
    def get_node(self):
        
        if not hasatt(self, "_node"):
            try:
                _node = Node.objects.get(id=self.pk)
            except ObjectDoesNotExist as e:
                msg = "Node with id:{} does not exist".format(self.pk)
                raise cmsexceptions.NodeDoesNotExist(msg)
            
        return self._node
    @property    
    def fields(self):
        """
        The field definitions are global instances that all classes have a
        reference to. This can become a problem if some fields have instance
        specific data so here we just create a copy of our own fields 
        and stick to using those instead.
        """
        
        if self._fields is None:
        
            self._fields = {}
            attribute_names = dir(self.__class__)
            for attribute_name in attribute_names:
                attribute = getattr(self.__class__, attribute_name)
                if isinstance(attribute,(CMSField)):
                    attribute = deepcopy(attribute)
                    self._fields.update({attribute_name: attribute})
        
        return self._fields         
        
    @property  
    def data(self):
        """
        Builds the data_dict for the page. Just iterates through the CMSFields
        and calls their get_values:
        """
        _data = {}
        
        for field_name, field_instance in self.fields.items():
            field_instance.initialize(page_id=self.pk, name=field_name)
            _data.update({field_name: field_instance.get_value()})
            
        return _data
        
        
    @property 
    def name(self):
        pass
    
    @property 
    def template(self):
        """
        The template to use is stored and overriden in multiple places and it 
        is resolved as follows:
        
        1) Try to get it from the node definition.
        2) from the page definition
        """
        
        
        
    
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
        
        
    def render(self):
        
        from django.http import HttpResponse
        return response()
    
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
    
    content = cmsfields.CMSTextField()
    another = cmsfields.CMSTextField()

class ListPage(Page):
    pass

class IndexPage(Page):
    pass