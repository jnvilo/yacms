from rest_framework import serializers
from mycms import models


class NodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Node
        fields = ["id", "title","path","created",
                  "modified","owner","page_type",
                  "parent"]
        
    
        
    
    
class PageSerializerBase(serializers.Serializer):
    
    node = NodeSerializer()
