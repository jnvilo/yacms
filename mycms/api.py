from pprint import pprint

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

    def get_serializer(self, *args, **kwargs):
        """
        The serializers are generated and stored in the PageRegistry.
        This just gets the serializer from there. 
        """

        """
        The name of a viewset is always the name + ViewSet so we can 
        find the name of the class by stripping away ViewSet
        """

        name = self.__class__.__name__[:-7]

        """
        The PageRegistry has the serializer built by BasePage.buildserializer()
        and on startapp, mycms.apps.MyCMSConfig.read() calls
        PageRegistry.get_default_serializers()
        """
        klass = PageRegistry.get_serializer(name)
        return klass(*args, **kwargs)

    def get_object(self):
        """
        Returns a page instance.
        """

        # load the Page class
        name = self.__class__.__name__[:-7]  # the name is taken from the class name
        PageClass = PageRegistry.get_pageclass(name)

        # get the CMSField Attributes.

        page = PageClass.load(self.pk, self.request)

        # get the value of the attributes
        return page.data

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a Page. 
        """

        pk = kwargs.get("pk", None)

        if pk is None:
            raise APIException(detail="pk is needed")

        self.pk = pk
        self.page_id = pk
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return Response(serializer.data)

        except Exception as e:
            raise APIException(e)

    def create(self, request, *args, **kwargs):

        print(args)
        print(kwargs)

        print(request.data)

        serializer = self.get_serializer(data=request.data)

        """
        calling is_valid runs the drf validation on the incoming data
        and modifies it. 
        """

        serializer.is_valid(raise_exception=True)
        pprint(serializer)
        serializer.save()

        return Response(data=serializer.data)


    def update(self, request, pk=None):
        print(request.data)
        print(pk)
        
        #Page updates by pk. The 
        
        
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        print(serializer.data)