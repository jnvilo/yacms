"""
A CMSField describes a page attribute. It provides a serializer so that 
it can be serialized. 
"""
from django.core.exceptions import ObjectDoesNotExist

from mycms  import models as cmsmodels
from mycms import serializers as cmsserializers
from mycms.serializers import NodeSerializer
from mycms import exceptions as cmsexceptions
from mycms.serializers import CMSTextFieldSerializer

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
    
    def initialize(self, page_id=None, name=None):
    
        assert page_id is not None, "page_id is required"
        assert name is not None, "name is required"
        
        self.page_id = page_id
        self.name = name
     
    
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
        
    
    
class CMSNodeField(CMSField):
    

    def get_object(self):
        node = cmsmodels.Node.objects.get(pk=self.page_id)
        return node
    
    def get_serializer(self):
        """
        Returns the serializer class.
        """
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
    
    serializer_class = CMSTextFieldSerializer
 
    
    def get_object(self):
        """
        Return an object which points to our pages node. 
        """
        
        try:
            node = cmsmodels.Node.objects.get(pk=self.page_id)
        except ObjectDoesNotExist as e:
            msg = "Failed to get CMSTextField because node with id={}".format(self.page_id)
            msg = msg + " could not be found."
            raise cmsexceptions.CMSFieldDoesNotExist(msg)
        
        content, c = cmsmodels.CMSModelTextField.objects.get_or_create(node=node,
                                                                       name=self.name)
        return content
    
    def get_serializer(self):
        return self.serializer_class
    

    
