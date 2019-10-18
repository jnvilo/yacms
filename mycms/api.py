from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .serializers import NodeSerializer
from .serializers import PageSerializerBase
from .models import Node

from .pages import Page
from .registry import PageRegistry
from django.http import HttpResponseBadRequest

class NodeViewSet(viewsets.ModelViewSet):
    
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    

class PageViewSet(viewsets.ViewSet):
    """
    This is just a standard viewset 
    """
    
    def get_serializer(self,instance):
        """
        The serializers are generated and stored in the PageRegistry.
        
        This just gets the serializer from there. 
        """
        
        #The name of a viewset is always the name + ViewSet so we can 
        #find the name of the class by stripping away ViewSet
        name = self.__class__.__name__[:-7]
        klass =  PageRegistry.get_serializer(name)
        return klass(instance)
    
    def get_object(self):
        """
        Returns a page instance.
        """
    
        #load the Page class
        name = self.__class__.__name__[:-7] #the name is taken from the class name
        PageClass = PageRegistry.get_pageclass(name) 
        
        #get the CMSField Attributes. 
        
        page = Page(self.pk)
        
        #get the value of the attributes 
        return page.data
        

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a Page. 
        """
        
        pk = kwargs.get("pk", None)
        
        if pk is None:
            raise APIException(detail="pk is needed")
            
        self.pk = pk
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        #serializer = PageSerializerBase(instance)
        data = serializer.data
        return Response(serializer.data)
    
