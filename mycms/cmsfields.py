"""
A CMSField describes a page attribute. It provides a serializer so that 
it can be serialized. 
"""

from mycms  import models as cmsmodels
from mycms import serializers as cmsserializers
from mycms.serializers import NodeSerializer

"""
   serializer_field_mapping = {
        models.AutoField: IntegerField,
        models.BigIntegerField: IntegerField,
        models.BooleanField: BooleanField,
        models.CharField: CharField,
        models.CommaSeparatedIntegerField: CharField,
        models.DateField: DateField,
        models.DateTimeField: DateTimeField,
        models.DecimalField: DecimalField,
        models.EmailField: EmailField,
        models.Field: ModelField,
        models.FileField: FileField,
        models.FloatField: FloatField,
        models.ImageField: ImageField,
        models.IntegerField: IntegerField,
        models.NullBooleanField: NullBooleanField,
        models.PositiveIntegerField: IntegerField,
        models.PositiveSmallIntegerField: IntegerField,
        models.SlugField: SlugField,
        models.SmallIntegerField: IntegerField,
        models.TextField: CharField,
        models.TimeField: TimeField,
        models.URLField: URLField,
        models.GenericIPAddressField: IPAddressField,
        models.FilePathField: FilePathField,
    }
"""

class CMSField(object):
    pass
    
class CMSNodeField(CMSField):
    
    def initialize(self, pk):
        self.pk = pk 
    
    def get_object(self):
        node, c = cmsmodels.Node.objects.get_or_create(self.pk)
        return node
    
    def get_serializer(self):
        return cmsserializers.NodeSerializer
    
    def get_value(self):
        """
        Converts the data into its internal representation. 
        """
        return self.get_object()
        
    def get_attribute(self):
        return obj
    
    def data(self):
        """
        Return the data representation. This is usually a string 
        or more specifically a json string.
        """
        SerializerClass = self.get_serializer()
        instance = self.get_object()
        serializer = SerializerClass(instance)
        return serializer.data()
        
    
class CMSTextField(CMSField):
    
    def get_object(self):
        pass
    def get_serializer(self):
        
        pass
        

    
    
