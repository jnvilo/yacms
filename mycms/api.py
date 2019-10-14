from rest_framework import viewsets
from .serializers import NodeSerializer
from .serializers import PageSerializerBase
from .models import Node

from .pages import Page


class NodeViewSet(viewsets.ModelViewSet):
    
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
        


class PageViewSet(viewsets.ViewSet):
    
 
    def get_object(self):
        """
        Returns a page instance. 
        """
        
        pass
    
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a Page. 
        """
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    