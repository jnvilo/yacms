"""
api specific to the category cmsapp.

This file should contain DRF code to implement API for the cmsapp. 

URL routing  is done automatically for any class and it is of the 
following format:

../api/v1/<name_of_class.lower()>/ and they need to be based on 
viewsets.ModelViewSet
"""

        
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from mycms.models import CMSNode



from .serializers import CMSNodeModelSerializer
from rest_framework import viewsets

class CMSNodeViewSet(viewsets.ModelViewSet):
        
    api_base_name = "myviewset"
    permission_classes = (IsAuthenticated,)
    queryset = CMSNode.objects.all()
    serializer_class =  CMSNodeModelSerializer
    
    
def list_classes():
    pass


STATUSES = ( ("1","on"),("0","off"),)

class Category(viewsets.ViewSet):
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    owner = serializers.CharField(max_length=256)
    status = serializers.ChoiceField(choices=STATUSES, default='New')
    
    def create(self, validated_data):
        return Task(id=None, **validated_data)
    
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
            return instance    
    
    