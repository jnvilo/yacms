import os
from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import routers
from django.utils.text import slugify
from django.shortcuts import render
from mycms import cmsfields
from .exceptions import NodeDoesNotExist
from .exceptions import PageDoesNotExist
from mycms import exceptions as cmsexceptions
from .utils import sanitize_path
from .models import Node
from .models import PageType
from .serializers import PageSerializerBase
from .registry import PageRegistry

from .cmsfields import CMSField
from .cmsfields import DebugInfoField


class BasePage(metaclass=PageRegistry):
    @classmethod
    def get_name(cls):
        pass

    @classmethod
    def get_template(cls):
        pass

    @classmethod
    def get_display_name(cls):
        return getattr(cls.Meta, "name", None) if hasattr(cls, "Meta") else None

    @classmethod
    def get_base_path(cls):
        return getattr(cls.Meta, "base_path", None) if hasattr(cls, "Meta") else None

    @classmethod
    def get_template(cls):
        return getattr(cls.Meta, "template", None) if hasattr(cls, "Meta") else None

    @classmethod
    def build_serializer(cls):
        """
        Builds the root serializer for this class based on the 
        CMSField definitions. 
        """
        name = "{}Serializer".format(cls.__name__)
        attribute_names = dir(cls)
        attrs = {}

        """
        All Page subclassses would have one or more field defnitions 
        at the top of the page. (Does not have to be at the top).
        
        class CustomPage(Page):
        
            content = cmsfields.CMSContentField()
            node = cmsfields.CMSNodeField()
        
        We iterate through the class attributes and filter out anything that is
        subclass of a CMSField and get its serializer class which then 
        gets added as an instance attribute. 
        """

        for attribute_name in attribute_names:
            attribute = getattr(cls, attribute_name)
            if isinstance(attribute, (CMSField)) and attribute.is_serializable:
                serializer = attribute.get_serializer()

                """
                Now add an instance of the serializer for the field. 
                Note that this could also just be a serializer.Field attribute. 
                """

                attrs.update({attribute_name: serializer()})

        print(attrs)
        SerializerClass = type(name, (PageSerializerBase,), attrs)

        return SerializerClass
        # return PageSerializerBase

    @classmethod
    def build_viewset(cls):
        from .api import PageViewSet

        class_name = "{}ViewSet".format(cls.__name__)
        class_dict = {"serializer_class": cls.build_serializer()}
        ViewClass = type(class_name, (PageViewSet,), class_dict)
        return ViewClass


from copy import deepcopy


class Page(BasePage):

    node = cmsfields.CMSNodeField()
    debuginfo = cmsfields.DebugInfoField()

    def __init__(self, node, request, *args, **kwargs):
        self.pk = node.pk
        self._node = node
        self._fields = None
        self.request = request

    @classmethod
    def load(cls, nodeinfo, request, *args, **kwargs):
        """
        creates a Page instance for the given path. Raises PageDoesNotExist 
        exception when the path could not be loaded. 
        """

        def load_node_by_path(nodeinfo):
            try:
                path = sanitize_path(nodeinfo)
                node = Node.objects.get(path=path)

            except ObjectDoesNotExist as e:
                msg = "Node with pk: {} does not exist.".format(nodeinfo)
                raise cmsexceptions.NodeDoesNotExist(msg)

            return path, node

        if isinstance(nodeinfo, Node):
            # ok no work need to be done , node is loaded
            pass

        else:
            # could be a path or an int strng.
            try:
                pk = int(nodeinfo)
                node = Node.objects.get(pk=pk)
            except TypeError as e:
                # the nodeinfo could not be converted to an int.
                # this might mean that it is a path string. Try to load it
                # via path.
                path, node = load_node_by_path(nodeinfo)
            except ValueError as e:
                path, node = load_node_by_path(nodeinfo)

        try:
            klass_name = node.page_type.class_name
            PageClass = PageRegistry.get_pageclass(klass_name)
            instance = PageClass(node, request)
            return instance

        except ObjectDoesNotExist as e:
            raise PageDoesNotExist("{} could not be found".format(path))

    def get_node(self):
        """
        Load the node for the given pk. This is not really needed since 
        we now have self._node always populated from the instantiation of 
        the class. 
        
        """
        if not hasattr(self, "_node"):
            try:
                _node = Node.objects.get(id=self.pk)
            except ObjectDoesNotExist as e:
                msg = "Node with id:{} does not exist".format(self.pk)
                raise cmsexceptions.NodeDoesNotExist(msg)

        return self._node

    @property
    def id(self):
        """
        Returns the page ID. The page id is exactly 
        """
        node = self.get_node()
        return node.id

    @property
    def fields(self):
        """
        The field definitions are global instances that all classes have a
        reference to. This can become a problem if some fields have instance
        specific data so here we just create a copy of our own fields 
        and stick to using those instead.
        """

        """
        This is not needed over here anymore because it is.,
        
        
        
        """

        if self._fields is None:

            self._fields = {}
            attribute_names = dir(self.__class__)
            for attribute_name in attribute_names:
                attribute = getattr(self.__class__, attribute_name)
                if isinstance(attribute, (CMSField)):
                    attribute = deepcopy(attribute)
                    self._fields.update({attribute_name: attribute})

        return self._fields

    @property
    def data(self):
        """
        Builds the data_dict for the page. Just iterates through the CMSFields
        and calls their get_values:
        """
        _data = {}

        for field_name, field_instance in self.fields.items():
            field_instance.initialize(page=self, name=field_name)
            value = field_instance.get_value()

            _data.update({field_name: value})

        return _data

    @property
    def name(self):
        pass

    def get_template(self):
        """
        The template to use is stored and overriden in multiple places and it 
        is resolved as follows:
        
        1) Try to get it from the node definition.
        2) from the page definition
        3) If not then use the  <classname>.html.lower()
        """

        node = self.get_node()
        if node.template:
            return node.template
        elif hasattr(self, "template"):
            return self.template
        else:
            classname = self.__class__.__name__
            template = "mycms/{}.html".format(classname.lower())
            return template

    def render(self):

        return render(self.request, self.get_template(), self.data)

    def page_dict(self):

        pass


class PageData(object):
    """
    Encapsulates Page attributes that are to be sent
    to the template. 
    """


class TemplateAttributes(object):
    pass


class ViewSet(object):
    pass


class ArticlePage(Page):

    content = cmsfields.CMSTextField()
    another = cmsfields.CMSTextField()


class ListPage(Page):
    pass


class IndexPage(Page):
    pass
