import os
from  . pages import Page
from .pages import TemplateAttributes
from .pages import ViewSet


from . serializers import PageSerializerBase
from . serializers import NodeSerializer

def make_viewset(page_class, attribs):
    """
    Creates a viewset for a Page class. 
    
    page_class is a type Page or is a sublclass of mycms.Pages.Page. Page 
    contains a Meta with attributes that are subclasses of CMSField.
    """
    
    serializer_class = ake_serializer(page_class, attribs)
    
    klass_dict = { "serializer_class": m}
    ViewClass = type(cls.__name__, (viewsets.ViewSet),  klass_dict )
    return ViewClass    


    