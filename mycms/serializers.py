from pprint import pprint

from rest_framework import serializers
from rest_framework.exceptions import APIException


from django.core.exceptions import ObjectDoesNotExist
from mycms import models as cmsmodels

from .registry import PageRegistry


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = cmsmodels.Node
        fields = [
            "id",
            "title",
            "path",
            "created",
            "modified",
            "owner",
            "page_type",
            "parent",
        ]


class PageSerializerBase(serializers.Serializer):

    node = NodeSerializer()

    def get_page_class(self):

        class_name = self.get_page_class_name()
        PageClass = PageRegistry.get_pageclass(class_name)
        return PageClass

    def get_page_class_name(self):
        class_name = self.__class__.__name__[:-10]
        return class_name

    def validate(self, data):
        """
        Ensure that the passed data parameters conform to the fields 
        definition
        """

        declared_fields = self.fields
        # declared_fields is a dictionary of CMSFields.

        # At the least, the declared_fields must exist.
        for name in declared_fields.keys():
            if name not in data.keys():
                msg = "entry {} is missing from the POST param ".format(name)
                raise APIException(defail=msg)

        return data

    def create(self, data):
        """
        To create, we get the data, and iterate through it matching
        the keys to our fields.
        
        An example of the expected data is a dictionary that can look like: 
        
        {            
            "node": {
                "id": 0,
                "title": "string",
                "path": "string",
                "created": "2019-10-19T09:32:28Z",
                "modified": "2019-10-19T09:32:28Z",
                "owner": 0,
                "page_type": 0,
                "parent": 0
            },
            "another": {
                "content": "string"
            },
            "content": {
                "content": "string"
            }
        }
        """

        """
        First create a Page instance.
        The name of the serializer class is <PageClass>Serializer 
        """

        if self.__class__.__name__ in ["Page", "BasePage"]:
            class_name = self.get_page_class_from_data(data)

        """
        This is a hack to either insert a default page_type or fix the 
        page_type object back to just an integer since at this point
        serializer.is_valid() was already called which means the FK 
        values have been deserialized into their model equivalents. 
        
        We must turn them beack into their default integer type
        so that we can then send the node data to be serialized again.
        """
        try:
            page_type_data = data["node"]["page_type"]

            data["node"]["page_type"] = page_type_data.id
        except KeyError as e:
            # no page type.
            class_name = self.get_page_class_name()
            pagetype = cmsmodels.PageType
            page_type_obj = pagetype.objects.get(class_name=class_name)
            data["node"]["page_type"] = page_type_obj.id

        try:
            parent = data["node"]["parent"]
            data["node"]["parent"] = parent.id
        except KeyError as e:

            class_name = self.get_page_class_name()
            root_path = Node.objects.get(path="/")
            parent_node_obj, c = Node.objects.get_or_create(
                path="/lost_and_found", title="Loast And Found", parent=root_path
            )
            data["node"][parent] = parent_node_obj.id

        """
        The keys match to the defined CMSFields with the Page subclass. 
        The node is a default entry and should always exist. 
        """

        # We need to ensure that the Node is the first to be created. Here we
        # use the NodeSerializer , but instead of using self.NodeSerializer()
        # we get the copy of the instance from self.fields and use that
        # instead in order to avoid race conditions when using the class
        # global instance.

        node_field_instance = self.fields.get("node")

        SerializerClass = node_field_instance.__class__
        serializer = SerializerClass(data=data["node"])
        serializer.is_valid()
        serializer.validated_data
        # serializer.create()
        node = serializer.save()

        result = {"node": node}

        # TODO: This is VALIDATION CODE. Refactor it into validate()
        # so as to do the same like in drf.
        for name, instance in self.fields.items():
            if name != "node":
                # skip the node attribute since it
                # it already created
                value = data.get(name, None)
                if value is None:
                    msg = "{} requires {} "
                    msg = msg.format(self.__class__.__name__, name)
                    msg = msg + (
                        "to be a type of class type(instance) but it was "
                        "not found in the data passed to the create.  "
                        "Check your POST parameters."
                    )
                    raise AttributeError(msg)
                else:
                    SerializerClass = instance.__class__
                    serializer = SerializerClass(data=data[name])
                    # serializer.validate()
                    if serializer.is_valid():
                        serializer.validated_data
                    else:
                        msg = "Validation error for: {}"
                        raise APIException(msg.format(instance.__class__))
                    instance = serializer.save(
                        cmsmodelfield_node_9824=node, cmsmodelfield_name_9824=name
                    )

                    result.update({name: instance})

        return result

    def get_page_class_from_data(self, data):
        """
        The Page and BasePage class are generic pages so we have to get 
        the page_type from the node information. 
        """

        try:
            page_type_id = data["node"]["page_type"]

        except KeyError as e:
            detail = (
                """Page or BasePage class needs the node["page_type"] """
                """ in order to create a new page. """
            )
            raise APIException(detail=detail)

        except Exception as e:
            detail = (
                "Unhandled error in PageSerializerBase.create() "
                "at line 73. The original exception was: {e}".format(e)
            )
            raise APIException(detail=detail)

        try:
            page_type = cmsmodels.PageType.objects.get(pk=page_type_id)
            page_class = page_type.class_name
        except ObjectDoesNotExist as e:
            detail = "Requested Page type id: {} does not exist"
            raise APIException(detail=detail.format(page_type_id))

        return page_class


class CMSFieldSerializer(serializers.Serializer):
    pass


class CMSModelFieldSerializer(CMSFieldSerializer):
    def get_model(self):
        return self.Meta.model

    def create(self, validated_data):
        """
        This should create a new database entry. 
        """

        ModelClass = self.get_model()
        instance = ModelClass(**validated_data)
        instance.save()
        return instance


class CMSTextFieldSerializer(CMSModelFieldSerializer):

    content = serializers.CharField()

    class Meta:
        model = cmsmodels.CMSModelTextField
