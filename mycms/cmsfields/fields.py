"""
A CMSField describes a page attribute. It provides a serializer so that 
it can be serialized. 
"""
from django.core.exceptions import ObjectDoesNotExist

from mycms import models as cmsmodels
from mycms import serializers as cmsserializers
from mycms.serializers import NodeSerializer
from mycms import exceptions as cmsexceptions
from mycms.serializers import CMSTextFieldSerializer

from mycms import utils

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
    def __init__(self, *args, **kwargs):
        self.is_serializable = kwargs.get("is_serializable", True)

    def initialize(self, page=None, name=None):

        assert name is not None, "name is required"
        assert page is not None, "page instance is required"

        self.page = page
        self.name = name

    def get_value(self):
        """
        Get the value of the object. At its most basic form, this just returns
        the object. 
        """
        return self.get_object()

    def get_data(self):
        """
        Return the data representation. This is usually a string 
        or more specifically a json string.
        """
        SerializerClass = self.get_serializer()
        instance = self.get_object()
        serializer = SerializerClass(instance)
        return serializer.data()

    def __str__(self):
        raise NotImplementedError(
            "{} does not implement __str__".format(self.__class__.__name__)
        )


class CMSNodeField(CMSField):
    def get_object(self):
        node = cmsmodels.Node.objects.get(pk=self.page.pk)
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
            node = cmsmodels.Node.objects.get(pk=self.page.pk)
        except ObjectDoesNotExist as e:
            msg = "Failed to get CMSTextField because node with id={}".format(
                self.page_id
            )
            msg = msg + " could not be found."
            raise cmsexceptions.CMSFieldDoesNotExist(msg)

        content, c = cmsmodels.CMSModelTextField.objects.get_or_create(
            cmsmodelfield_node_9824=node, cmsmodelfield_name_9824=self.name
        )
        return content

    def get_serializer(self):
        return self.serializer_class

    def __str__(self):
        """
        raw string representation
        """
        return self.content.content

    def __str__(self):
        pass


class DebugInfoField(CMSField):
    """
    A field to provide debugging attributes. This exposes many 
    page attributes usually should not be available to the 
    template. 
    """

    def __init__(self, *args, is_serializable=False):

        self.is_serializable = utils.get_boolean_from_string(is_serializable)

    def get_value(self):
        """
        Returns debug information
        """
        # For future improvement, modify such that page is not in "self"
        # but rather it should be in a FieldContext dictionary. which is
        # only accessible via get_field_context and set_field_context.

        if self.page is None:
            msg = (
                "{}.get_value() requires the instance of "
                "CMSPage as a named parameter to be passed"
                "into the DebugInfoField".format(self.__class__.__name__)
            )
            raise cmsexceptions.CMSFieldError(msg)

        data = {"template": self.page.get_template(), "node": self.page.get_node()}

        return data
