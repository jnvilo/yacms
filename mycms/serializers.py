from rest_framework import serializers
from mycms import models


class PageSerializerBase(serializers.Serializer):
    pass

class NodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Node
        fields = ["id", "title","path","created","modified","owner","page_type","parent"]
        
    
        