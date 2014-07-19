from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from django.http import JsonResponse 
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify

import yacms
from yacms.models import Paths
from yacms.models import Pages
from yacms.exceptions import IncompatiblePageClass
from yacms.exceptions import PageClassNotFound
from yacms.exceptions import PageActionNotFound


from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from django.core.cache import cache


_page_class_map = {}


def register(page_type, page_class):
    if not  issubclass(page_class, BaseView):
        msg = "{} is not subclass PageView".format(page_class)
        raise IncompatiblePageClass(msg)
        
    _page_class_map[page_type] = page_class
    
    
def get_page_class(page_type):  
    PageClass = _page_class_map.get(page_type, None)
    
    if PageClass:
        return PageClass
    else:
        msg = "Could not find class to handle page_type: {}"
        raise PageClassNotFound(msg.format(page_type))
    
    
    
def get_pageview(path):
    
    from yacms.models import Paths, Pages
    
    try:
        page = Pages.objects.get(path__path = path)
        return page.view
    
    except ObjectDoesNotExist as e: 
        return None

class BaseView(object):
    
    """
    Base page view. Implements loading and editing page.    
    """
    response_dict = {}
    
    def __init__(self, page_obj):
        
        self.page_obj = page_obj
        #if hasattr(self, "META") and hasattr(self.META, "template"):
                #self.template = self.META.template
        #else:
            #self.template = "/yacms/{}.html".format(self.__class__.__name__.lower())
        self.update_response_dict("page", self.page_obj)
        self.update_response_dict("pageview", self)
            
    @property
    def page_obj(self):
        return self._page_obj

    @page_obj.setter
    def page_obj(self, value):
        self._page_obj = value
        
    def update_response_dict(self,name, value):
        self.response_dict.update({name:value})
    
    def response(self, request, **kwargs):
        #see what the action is.
        action =  request.GET.get("action", None)
        if action: 
            return self.exec_action(request, **kwargs)    
        else:
            #nothing to do but to just return the page.
            
            flags_list = ["show_edit", "show_debug"]
            
            
            template = "yacms/{}".format(self.page_obj.template)
            return render_to_response(template, self.response_dict,
                                       context_instance=RequestContext(request))
        
    def make_page(self, title, slug, page_type):
        
        #Here we create a page and return that page object.
        
        
        path = self.page_obj.path.path
        
        if slug is None:
            slug = slugify(title)
      
        if path.endswith("/"):
            path = path.rstrip("/")
        
        
        page_path = "{}/{}".format(path, slug)    
        
        #we create a new path. Note we do not need to add the parent
        #since this is calculated in the save of the Paths model.
        page_path_obj, created = Paths.objects.get_or_create(path=page_path)
        
        if not created:
            msg = "Path {} already exists".format(page_path_obj.path)
            raise yacms.exceptions.PathExists(msg)
        
        page = Pages()
        page.title = title
        page.slug = slug
        page.path = page_path_obj
        page.page_type=page_type
        page.save()
        
        return page
    
    
    def exec_action(self, request, **kwargs):
        
        action =  request.GET.get("action", None)
        
        if action == "make_page":
            GET = request.GET
            POST = request.POST 
                
            title = POST.get("title", None)
            slug = POST.get("slug", None)
            page_type = POST.get("page_type", None)

            if request.is_ajax():
                try:
                    new_page_obj =  self.make_page(title, slug, page_type)            
                    #Create a page_ajax response dict that contains just
                    #enough of the data needed.
                    d = { "path": new_page_obj.path.path , 
                          "title":new_page_obj.title, 
                          "slug": new_page_obj.slug, 
                          "date_created": new_page_obj.date_created,
                          "date_modified" : new_page_obj.date_modified, 
                          "page_type": new_page_obj.page_type,
                          "absolute_url": new_page_obj.get_absolute_url(),
                          }                
                
                    return JsonResponse(data=d)
                except yacms.exceptions.PathExists as e:
                    
                    return JsonResponse({ "error_msg": e.message})
                    
        elif action == "toggle_publish":
            
            if request.is_ajax():
                published = self.page_obj.published
                
                if published:
                    self.page_obj.published=False
                else:
                    self.page_obj.published=True
                
                self.page_obj.save()
                
                data = {"published": self.page_obj.published}
                return JsonResponse(data=data)
        
        #This expects to recieve a page_form 
            
            #make the page
            
            # and return the page.
        else:
            
            return HttpResponse("Application Error: Action requested is not possible.")
    def toggle_frontpage(self):
        pass
            
        
    def __getattr__(self, value):
        #Try to get the info from the page_obj
        
        if hasattr(self.page_obj, value):
            return getattr(self.page_obj, value)
        
        else:
            raise AttributeError("Attribute {} Not Found.".format(value))
        
        
        
    def get_child_categories(self):
        
        path_obj = self.page_obj.path
        children = Pages.objects.filter(path__parent=path_obj, page_type="CATEGORYVIEW").order_by("path")       
        return children
    

    def iter_child_categories(self):
        
        path_obj = self.page_obj.path
        children = Pages.objects.filter(path__parent=path_obj, page_type="CATEGORYVIEW")
        
        for each in children:
            yield each.view



    def iter_child_html_pages(self):
        
        path_obj = self.page_obj.path
        children = Pages.objects.filter(path__parent=path_obj, page_type="HTMLVIEW").order_by("date_modified")
        
        for each in children:
            yield each.view
            
            
    def iter_frontpage_pages(self):
        children = Pages.objects.filter(page_type="HTMLVIEW").filter(frontpage=True).order_by("date_modified")    
        for each in children:
            yield each.view
        
    def get_absolute_url(self):
        return self.page_obj.get_absolute_url()
    
    def iter_parent_pages(self):
        x = self.page_obj.path.path
        path_parts =  x.split("/")[1:len(x.split("/"))-1]
        
        complete_path = ""
        for each in path_parts:
            try:
                
                complete_path = complete_path + "/" + each 
                each_obj = Pages.objects.get(path__path = complete_path)
                
                yield each_obj
                
            except ObjectDoesNotExist as e:
                yield None
    

                
    
        

        