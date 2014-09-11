from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
# Create your views here.

from . models import Pages




def sitemap(request):
    
    pass

def page(request, **kwargs):
    
    """The main entry view into the CMS. It will try to load
    the path and let it do the rest of the work."""
    
    path = kwargs.get("path", "/cms")
    if not path.startswith("/"):
        path = "/" + path    
    try:
        
        """
        
        TODO:
        
        Optimize this by creating  a CachedPageView class. 
        
        The CachedPageView class simply implements a wrapper 
        around the yacmls.pageview.* classes so that if the request 
        is just a simple get. Then we return a cached page instead.
        
        
        """
        import cProfile, pstats, StringIO
        pr = cProfile.Profile()
        pr.enable()        
        page = Pages.objects.get(path__path=path)
        r =  page.response(request, **kwargs)
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())        

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