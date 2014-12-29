from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import logging
import pathlib
import os
from PIL import Image
import threading

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.http import JsonResponse


from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
# Create your views here.

from . models import Pages


logger = logging.getLogger(name="yacms.views")


def sitemap(request):
    
    pass

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def filedelete(request, **kwargs):
    
    mylock = threading.Lock()
    
    with mylock:
        from django.conf import settings
        assets_dir = settings.ASSETS_DIR
        path = kwargs.get("path", None).lstrip("/")
        
        fullpath = pathlib.Path(pathlib.Path(assets_dir), path)
        
        if request.method == "DELETE":
            
            pass
    
    
    
            
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
    
        files = []
        filenames = os.listdir(fullpath.as_posix())
       
        
        for filename in filenames:
            
            p_filename = pathlib.Path(fullpath, filename)
    
            if not p_filename.is_dir():
                
                stat = os.stat(p_filename.as_posix())
                image_url =  url = "/assets/{}/{}".format(path, filename)
                thumbnail_url = "/assets/{}/thumbnails/{}".format(path, filename)
                delete_url = "/cms/{}/mediadelete_endpoint/{}".format(path, filename)
                
        
                file_dict = { "name": filename , 
                              "size": stat.st_size,
                              "url": image_url, 
                              "thumbnailUrl": thumbnail_url, 
                              "deleteUrl": delete_url,
                              "deleteType": "DELETE" }
                
                files.append(file_dict)
                
        return JsonResponse({'files': files})
            
        
    

@csrf_exempt
def fileupload(request, **kwargs):
    
    mylock = threading.Lock()
    
    with mylock:
        from django.conf import settings
        assets_dir = settings.ASSETS_DIR
        path = kwargs.get("path", None).lstrip("/")
        
        fullpath = pathlib.Path(pathlib.Path(assets_dir), path)
        
        if not fullpath.exists():
            os.makedirs(fullpath.as_posix())
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
    
        files = []
        filenames = os.listdir(fullpath.as_posix())
       
        
        for filename in filenames:
            
            p_filename = pathlib.Path(fullpath, filename)
    
            if not p_filename.is_dir():
                
                stat = os.stat(p_filename.as_posix())
                image_url =  url = "/assets/{}/{}".format(path, filename)
                thumbnail_url = "/assets/{}/thumbnails/{}".format(path, filename)
                delete_url = "/cms/{}/mediadelete_endpoint/{}".format(path, filename)
                
        
                file_dict = { "name": filename , 
                              "size": stat.st_size,
                              "url": image_url, 
                              "thumbnailUrl": thumbnail_url, 
                              "deleteUrl": delete_url,
                              "deleteType": "DELETE" }
                
                files.append(file_dict)
                
        return JsonResponse({'files': files})
            
        
        
def page(request, **kwargs):
    
    """The main entry view into the CMS. It will try to load
    the path and let it do the rest of the work."""
    
    
    
    path = kwargs.get("path", "/cms")
    if not path.startswith("/"):
        path = "/" + path    
    try:
        logger.debug("Recieved request for: {}".format(path))        
        
        """
        
        TODO:
        
        Optimize this by creating  a CachedPageView class. 
        
        The CachedPageView class simply implements a wrapper 
        around the yacmls.pageview.* classes so that if the request 
        is just a simple get. Then we return a cached page instead.
        
       
        """
        #import cProfile, pstats, StringIO
        #pr = cProfile.Profile()
        #pr.enable()        
      
        page = Pages.objects.get(path__path=path)
        
        r =  page.response(request, **kwargs)
        #pr.disable()
        #s = StringIO.StringIO()
        #sortby = 'cumulative'
        #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        #ps.print_stats()
        #print(s.getvalue())        

        return r
    except ObjectDoesNotExist as e:
        """
        Initially the /admin path is not created. We create it here.
        """
        if path == "/admin":
            p = Pages.get_or_create_from_request(request, 
                                            path="/admin",
                                            title="CMS Administration",
                                            page_type="ADMINVIEW")
        
        #also create the root path if it does not yet exist
        if path == "/":            
            p = Pages.get_or_create_from_request(request, 
                                                path="/",
                                                title="cms",
                                                page_type="CATEGORYVIEW")
            
            return p.response(request, **kwargs)
        return HttpResponseNotFound("Page does not exist")
        

def index(request, **kwargs):
    
    return HttpResponse("Index page")
