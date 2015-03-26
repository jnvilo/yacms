from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import logging
import pathlib
import os
from PIL import Image
import threading
import datetime

from bs4 import BeautifulSoup
import simplejson as json
import threading

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.forms.models import model_to_dict
from django.http import Http404
from django.core.files.uploadedfile import UploadedFile

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

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


from loremipsum import get_paragraphs
from yacms.creole import creole2html

from . serializers import CMSPageTypesSerializer
from . serializers import CMSContentsSerializer
from . serializers import CMSEntrySerializer
from . serializers import CMSMarkUpSerializer
from . serializers import CMSTemplatesSerializer
from . serializers import CMSPathsSerializer
from . serializers import CMSEntryExpandedSerializer
from . serializers import LoremIpsumSerializer


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
        
        
        
def  get_static_files_dir():
    """
    Gets the static files directory.
    """
     
    for each in settings.STATICFILES_DIRS:
        if each.endswith("static"):
            return each
    else:
        return None
    
ASSETS_DIR = pathlib.Path(get_static_files_dir(),"assets")

if not ASSETS_DIR.is_dir:
    ASSETS_DIR.mkdir()
    
def index(request, **kwargs):    
    return HttpResponse("Index page")


class LoremIpsumAPIView(APIView):
    
    """Returns loremipsum paragraphs"""
    authentication_classes = (authentication.SessionAuthentication, 
                      authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
   
    def get(self, request, **kwargs):
        
        data = { "message": "You need to send a post."}
        return Response(data, status=status.HTTP_200_OK)
        
   
    def post(self, request, **kwargs):
        """Get X number of paragraphs"""
        serializer = LoremIpsumSerializer(data=request.data)
        if serializer.is_valid():
            num_paragraphs = request.data.get("num_paragraphs")
            
            paragraphs_list  = get_paragraphs(int(num_paragraphs))
            
            html = ""
            for paragraph in paragraphs_list:
                html += "{}\n\n".format(paragraph)
          
            data = {"content" : html }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
        
        

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
            
            cms_obj = CMSEntries.objects.get(id = serializer.data.get("id"))
            
            content = CMSContents()
            content.content = "No content. Edit me."
            content.save()
            
            cms_obj.content.add(content)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        serializer = CMSEntrySerializer(data=request.data)
        
      
        
        format = kwargs.get("format", None)
        expand = self.request.QUERY_PARAMS.get('expand', None)
        
        id = request.data.get("id", None)
        
        
        if not id:
            res = {"code": 400, "message": "PUT request requires an id parameter"}
            return Response(data=json.dumps(res), status=status.HTTP_400_BAD_REQUEST)            
        
        if serializer.is_valid():
            cmsentry_object = CMSEntries.objects.get(id=id)
            
            frontpage = cmsentry_object.frontpage
            published = cmsentry_object.published
            
            #Now update the cmsentry_object with the attributes from 
            #the request.data
            
            for key in request.data:
                
                if key == "date_created_epoch":
                    print("Recieved a date_created_epoch")
                    value = request.data.get("date_created_epoch")
                    created_datetime = datetime.datetime.utcfromtimestamp(int(value)/1000)
                    
                    cmsentry_object.date_created = created_datetime
                    
                    
                elif hasattr(cmsentry_object, key) and (key != "id"):
                    
                    value = request.data.get(key)
                    if value == "true":
                        value = True
                    if value == "false":
                        value = False
                    setattr(cmsentry_object, key, value)
            
            cmsentry_object.save()
            
            #if expand:
                
            #We return only the values that we have set. 

            return_dict = {}
            for key in request.data:
                if hasattr(cmsentry_object, key):
                    value = getattr(cmsentry_object, key)
            
                return_dict[key] = value
                
            return Response(return_dict, status=status.HTTP_200_OK) 
        else:
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
            
            print(serializer.data)
             
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
    
    def get_object(self,**kwargs):
        """
        returns a YACMSViewObject
        """
        path = kwargs.get("path", None)
        page_id = kwargs.get("page_id", None)
        
        try:
            if path:
                obj = YACMSViewObject(path=path)
            elif page_id:
                obj = YACMSViewObject(page_id=page_id)
            else:
                #Lets make path = "/" as default.
                obj = YACMSViewObject(path=u"/")
            return obj
        
        except ObjectDoesNotExist as e:
            
            if (path is None) or (path == u"/"): 
                #we are in /cms and it does not exist. We create it!!
                
                
                path_obj,_ = CMSPaths.objects.get_or_create(path="/")
               
                try:
                    pagetype_obj, _ = CMSPageTypes.objects.get_or_create(page_type="CATEGORY",
                                                                      text = "Category Page",
                                                                      view_class = "CategoryPage",
                                                                      view_template = "CategoryPage.html"
                                                                      )
                except MultipleObjectsReturned as e:
                    
                    logger.warn("Multiple PageType: CATEGORY found. Database is inconsistent. Returning the first one found.")
                    pagetype_obj = CMSPageTypes.objects.filter(page_type="CATEGORY")[0]
                    
                    
                try:
                    entry_obj, c= CMSEntries.objects.get_or_create(page_type=pagetype_obj,
                                                                 path=path_obj,
                                                                 title="Yet Another CMS.")
                except MultipleObjectsReturned as e:
                    msg = "Multiple CMSEntries for /cms found. Database is inconsistent. Using the first one found. "
                    logger.warn(msg)
                    
                    entry_obj = CMSEntries.objects.filter(path=path_obj)[0]
                    
                  
                
                obj = YACMSViewObject(path=u"/")
                return obj
            else:                                                     
                raise Http404("Page Does Not Exist.")
        
      
            
    
            
    def get(self,request, **kwargs):
        """Just get the page and return it."""
        
        obj = self.get_object(**kwargs)
        obj.request = request
        template = obj.template
        return render_to_response(template, {"view_object": obj})
        
    def post(self, request, **kwargs):
        print(request, kwargs)
        return HttpResponse("Not implemented")
        
    def put(self, request, **kwargs):
        print(request, kwargs)
        return HttpResponse("Not Implemented")
    
    
    
    
########################################################################
class  AssetsUploaderView(View):
    """Handles the uploading and deleting of images. Uses multiuploader AJAX plugin.
    made from api on: https://github.com/blueimp/jQuery-File-Upload
    """
        
    def _mkdir(self,newdir):
        """Copied from http://code.activestate.com/recipes/82465-a-friendly-mkdir/ """
        """works the way a good mkdir should :)
            - already exists, silently complete
            - regular file in the way, raise an exception
            - parent directory(ies) does not exist, make them as well
        """
        if os.path.isdir(newdir):
            pass
        elif os.path.isfile(newdir):
            raise OSError("a file with the same name as the desired " \
                          "dir, '%s', already exists." % newdir)
        else:
            head, tail = os.path.split(newdir)
            if head and not os.path.isdir(head):
                self._mkdir(head)
            #print "_mkdir %s" % repr(newdir)
            if tail:
                os.mkdir(newdir)

    #----------------------------------------------------------------------
    def  get(self, request, **kwargs):
       
        """ 
        We assume we have a GET
        According to https://github.com/blueimp/jQuery-File-Upload/wiki/Setup
        we have to return a list of the images in the dir as follows:



        {"files": [
          {
            "name": "picture1.jpg",
            "size": 902604,
            "url": "http:\/\/example.org\/files\/picture1.jpg",
            "thumbnailUrl": "http:\/\/example.org\/files\/thumbnail\/picture1.jpg",
            "deleteUrl": "http:\/\/example.org\/files\/picture1.jpg",
            "deleteType": "DELETE"
          },
          {
            "name": "picture2.jpg",
            "size": 841946,
            "url": "http:\/\/example.org\/files\/picture2.jpg",
            "thumbnailUrl": "http:\/\/example.org\/files\/thumbnail\/picture2.jpg",
            "deleteUrl": "http:\/\/example.org\/files\/picture2.jpg",
            "deleteType": "DELETE"
          }
        ]}        
        """ 
        
        
        assets_dir = ASSETS_DIR
        path = kwargs.get("path", None).lstrip("/")
        fullpath = pathlib.Path(pathlib.Path(assets_dir), path)        

        files = []
        
        try:
            filenames = os.listdir(fullpath.as_posix())
        except OSError as e:
            return  JsonResponse({'files': []}) 

        for filename in filenames:

            p_filename = pathlib.Path(fullpath, filename)

            if not p_filename.is_dir():

                stat = os.stat(p_filename.as_posix())
                image_url =  url = "/static/assets/{}/{}".format(path, filename)
                thumbnail_url = "/static/assets/{}/thumbnails/{}".format(path, filename)
                delete_url = "/cms/{}/assets_manager/{}".format(path, filename)


                file_dict = { "name": filename , 
                              "size": stat.st_size,
                              "url": image_url, 
                              "thumbnailUrl": thumbnail_url, 
                              "deleteUrl": delete_url,
                              "deleteType": "DELETE" }

                files.append(file_dict)

        return JsonResponse({'files': files})    
    
    
    #----------------------------------------------------------------------
    def  post(self, request, **kwargs):
        """"""
        return self.fileupload(request, **kwargs)
         
    
    def fileupload(self,request, **kwargs):
        
        mylock = threading.Lock()
        
        with mylock:
            from django.conf import settings
            assets_dir = ASSETS_DIR
            path = kwargs.get("path", None).lstrip("/")
            
            fullpath = pathlib.Path(pathlib.Path(assets_dir), path)
            
            if not fullpath.exists():
                self._mkdir(fullpath.as_posix())
            elif not fullpath.is_dir():
                #Fix this to return a proper json response.
                return HttpResponse("Error. Not full dir")
            
            thumbnailpath = pathlib.Path(fullpath, "thumbnails")
            
            if not thumbnailpath.exists():
                os.makedirs(thumbnailpath.as_posix())
            elif not thumbnailpath.is_dir():
                #Fix this to return a proper json response.
                return HttpResponse("Error. Not full dir")    
            
            if request.method == "POST":
                uploaded_file = request.FILES.get("files[]")
                
                filename = uploaded_file.name
        
                p_filename = pathlib.Path(fullpath, filename)
          
                with open(p_filename.as_posix(), 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)  
                
                #Now do the thumbail.
                try:
                    size = 256, 256
                    outfile =  pathlib.Path(thumbnailpath, filename)
                    im = Image.open(p_filename.as_posix())
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(outfile.as_posix(), "JPEG")
                except IOError as e:
                    return JsonResponse( { "error" : "cannot create thumbnail for {}".format(outfile)})        
                
                except Exception as e: 
                    return JsonResponse( { "error": "Unhandled exception: {}".format(outfile) })        
                    
                
                    
                stat = os.stat(p_filename.as_posix())
                image_url =  url = "/static/assets/{}/{}".format(path, filename)
                thumbnail_url = "/static/assets/{}/thumbnails/{}".format(path, filename)
                delete_url = "/cms/{}/assets_manager/{}".format(path, filename)
                
                files = []
                file_dict = { "name": filename , 
                                  "size": stat.st_size,
                                  "url": image_url, 
                                  "thumbnailUrl": thumbnail_url, 
                                  "deleteUrl": delete_url,
                                  "deleteType": "DELETE" }
                    
                files.append(file_dict)
                    
                return JsonResponse({'files': files}) 
            
    #----------------------------------------------------------------------
    def  delete(self,request, **kwargs):
        """"""
        path = kwargs.get("path", None).lstrip("/")
        filename=kwargs.get("filename",None).lstrip("/")
        fullpath = pathlib.Path(pathlib.Path(ASSETS_DIR), path)               
        
        
        p_filename = pathlib.Path(fullpath, filename)
        
        logger.debug("Going to delete, {}".format(p_filename.as_posix()))
        
        """We need to return a format as below:
            {"files": [
              {
                "picture1.jpg": true
              },
              {
                "picture2.jpg": true
              }
            ]}        
            """
        
        try:
            
            os.remove(p_filename.as_posix())

            files = [ { filename: True }]
            
            return JsonResponse({ 'files': files} )
            
        except Exception as e:
            
            
            return HttpResponse("Deleted")