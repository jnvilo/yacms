from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import logging
import pathlib
import os
from PIL import Image
import threading

from bs4 import BeautifulSoup
import simplejson as json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.forms.models import model_to_dict

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
# Create your views here.

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from rest_framework import filters
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


from loremipsum import generate_paragraphs
from creole import creole2html

from . serializers import CMSPageTypesSerializer
from . serializers import CMSContentsSerializer
from . serializers import CMSEntrySerializer
from . serializers import CMSMarkUpSerializer
from . serializers import CMSTemplatesSerializer
from . serializers import CMSPathsSerializer
from . serializers import CMSEntryExpandedSerializer


from .models import CMSPageTypes
from .models import CMSContents
from .models import CMSEntries
from .models import CMSMarkUps
from .models import CMSTemplates
from .models import CMSPaths


from . view_handlers import YACMSViewObject

logger = logging.getLogger(name="yacms.views")

try:
    import wingdbstub
except:
    pass
        

def index(request, **kwargs):    
    return HttpResponse("Index page")


class CMSPathsAPIView(APIView):
    """
    View to list PageTypes handled by the system
    """
    
    authentication_classes = (authentication.SessionAuthentication, 
                              authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """
        Get a list of all available PageTypes
        """
        
        format = kwargs.get("format", None)
        paths = CMSPaths.objects.all()
        serializer = CMSPathsSerializer(paths, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CMSPathsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CMSPageTypesAPIView(APIView):
    """
    View to list PageTypes handled by the system

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """
        Get a list of all available PageTypes
        """
        
        format = kwargs.get("format", None)
        pagetypes = CMSPageTypes.objects.all()
        serializer = CMSPageTypesSerializer(pagetypes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CMSPageTypesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CMSMarkUpsAPIView(APIView):
    """
    View to list PageTypes handled by the system

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = (authentication.SessionAuthentication, 
                              authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """
        Get a list of all available PageTypes
        """

        format = kwargs.get("format", None)
        pagetypes = CMSMarkUps.objects.all()
        serializer = CMSMarkUpSerializer(pagetypes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CMSMarkUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CMSTemplatesAPIView(APIView):
    """
    View to list PageTypes handled by the system

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """
        Get a list of all available PageTypes
        """

        format = kwargs.get("format", None)
        pagetypes = CMSTemplates.objects.all()
        serializer = CMSTemplatesSerializer(pagetypes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CMSTemplatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import django_filters
class CMSEntriesFilter(django_filters.FilterSet):
    
    class Meta:
        model = CMSEntries
        fields = ['id','page_type', 'slug', 'date_created','published', 'frontpage', 'date_created']
                  

class CMSEntriesROAPIView(generics.ListAPIView):
    
    queryset = CMSEntries.objects.all()
    serializer_class = CMSEntrySerializer
    filter_class = CMSEntriesFilter
    permission_classes = (IsAuthenticated,)
    
    
    

class CMSEntriesAPIView(APIView):
    """
    View to list PageTypes handled by the system

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)

    def get(self, request, **kwargs):
        """
        Get a list of all available PageTypes
        """
        format = kwargs.get("format", None)
        parent_id  = self.request.QUERY_PARAMS.get('parent', None)
        page_id = self.request.QUERY_PARAMS.get('id', None)
        page_type_id = self.request.QUERY_PARAMS.get('page_type', None)
        expand=self.request.QUERY_PARAMS.get('expand', None)
        
        cmsentries = CMSEntries.objects.all()
        
        if parent_id is not None:
            cmsentries = cmsentries.filter(path__parent__id=parent_id) 
            
        if page_type_id:
            cmsentries = cmsentries.filter(page_type=page_type_id)
        
        if page_id is not None:
            cmsentries = cmsentries.filter(id=page_id)
    
        if expand:
            serializer = CMSEntryExpandedSerializer(cmsentries, many=True)
        else:
            serializer = CMSEntrySerializer(cmsentries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CMSEntrySerializer(data=request.data)
        
        #TODO: Update this piece of code so that it will create a proper 
        #      entry
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CMSContentsAPIView(APIView):
    """
    View to list PageTypes handled by the system

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """
        Get a list of all available PageTypes
        """

        format = kwargs.get("format", None)
        pagetypes = CMSContents.objects.all()
        
        
        
        page_id = self.request.QUERY_PARAMS.get('id', None)
        
        if page_id is not None:
            pagetypes = pagetypes.filter(id=page_id);
            
        
        serializer = CMSContentsSerializer(pagetypes, many=True)
        
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CMSContentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        
       
        serializer = CMSContentsSerializer(data=request.data)
        
        id = request.data.get("id", None)
        
        if not id:
            res = {"code": 400, "message": "PUT request requires an id parameter"}
            return Response(data=json.dumps(res), status=status.HTTP_200_OK)            
         
        if serializer.is_valid():
            cmscontent_object = CMSContents.objects.get(id=id)
            cmscontent_object.content = request.data.get("content")
            cmscontent_object.save()
            
            include_html = request.GET.get("include_html", None)
            if include_html:
                #Custom pack results:
                cmscontent_dict = model_to_dict(cmscontent_object)
                cmscontent_dict["html"] = cmscontent_object.html
                
                return Response(cmscontent_dict, status=status.HTTP_202_ACCEPTED)
            else:
                serializer = CMSContentsSerializer(cmscontent_object)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        
   
    
class CMSIndexView(APIView):
    """
    The index view of a YACMS website. 
    
    url: /cms. 
    
    This is a special page since it needs to exist before any other
    categories or pages can be created. 
    
    To create a new page , we need at minimum to post 
    
    title:
    page_type:
    
    """
    
    def get(self, request, **kwargs):
        pass
    
    
class CMSPageView(View):
    """
    The main interface to the website.  
    """
    
    def get_object(self, **kwargs):
        """
        returns a YACMSViewObject
        """
        path = kwargs.get("path", None)
        page_id = kwargs.get("page_id", None)
        
        if path:
            obj = YACMSViewObject(path=path)
        elif page_id:
            obj = YACMSViewObject(page_id=page_id)
        else:
            #Lets make path = "/" as default.
            obj = YACMSViewObject(path=u"/")
        return obj
        
    
            
    def get(self,request, **kwargs):
        """
        Just get the page and return it.
        """
        obj = self.get_object(**kwargs)
        
        template = obj.template
        
        return render_to_response(template, {"view_object": obj})
        
        
    
    def post(self, request, **kwargs):
        pass
        
    def put(self, request, **kwargs):
        pass
    
