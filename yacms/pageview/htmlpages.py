from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from creole import creole2html
from random import randrange
import loremipsum

from bs4 import BeautifulSoup
from django.http import JsonResponse

from django.core.cache import cache


from .base import BaseView
from .base import register
from .creole_macros import code
from .creole_macros import pre
from .creole_macros import html

class PageView(BaseView):
    
    def html(self):
        
        content = self.page_obj.content
        return creole2html(content, debug=False, parser_kwargs={}, 
                   emitter_kwargs={}, block_rules=None, 
                   blog_line_breaks=True, macros={ "code": code, 
                                                   "pre": pre,
                                                   "html": html}, 
                   verbose=None,  stderr=None)
        
        
    def exec_action(self, request, **kwargs):
        
        
        action = request.GET.get("action", None)
        
        if action == "save_page":
            
            content = request.POST.get("content")
            if request.is_ajax():
                
                self.page_obj.content = content
                self.page_obj.save()
            
                data = { "message" : "Successfully saved: {}".format(self.page_obj.title),
                         "page_html" : self.html()}
            
                return JsonResponse(data=data)
            
            
        if action == "get_ipsum":
            
            if request.is_ajax():
                c = randrange(10)   
                p = loremipsum.get_paragraphs(c+5)
            
                paragraphs = "\n\n".join(p)
            
                data = { "paragraphs" : paragraphs}
            
                return JsonResponse(data=data)
        
        
        
        if action == "toggle_frontpage":
            
            if request.is_ajax():
                frontpage = self.page_obj.frontpage
                
                if frontpage:
                    self.page_obj.frontpage = False
                else:
                    self.page_obj.frontpage = True
                    
                self.page_obj.save()
                
                data = {"frontpage": self.page_obj.frontpage }
                return JsonResponse(data=data)
        
        if action == "modify_page_data":
            
            if request.is_ajax():
                
                date = request.get("date_submitted")
                pass
                
                
        if action == "save_meta_data":
            
            if request.is_ajax():
                
                page_header_title = request.POST.get("json_page_header_title", None)
                date_submitted = request.POST.get("json_date_submitted", None)
                date_modified = request.POST.get("json_date_modified", None)
                meta_header = request.POST.get("json_meta_header", None)
                
                
                if page_title:
                    self.page_obj.page_header_title = page_header_title
                if date_submitted:
                    self.page_obj.date_submitted = date_submitted
                if date_modified:
                    self.page_obj.date_modified = date_modified
                if meta_header:
                    self.page_obj.meta_header = meta_header
                    
                self.page_obj.save()
                
                return JsonResponse(data={"success": "Successfully Saved data."})
                
            
                
            
        return super(PageView, self).exec_action(request, **kwargs)


    
    def introduction(self):
        
        path = self.page_obj.path.path
        title = self.page_obj.title
        
        key_name = "{0}:{1}:{2}".format("introduction",path, title)  
        
        value = cache.get(key_name)
        
        if not value:
    
            html = self.html()
            
            soup = BeautifulSoup(html)
            
            p = soup.find("p")
            
            value = str(p)
            value = value.lstrip("<p>")
            value = value.rstrip("</p>")
            
            cache.set(key_name, value)
            
        return value
        
        
        
        

register("HTMLVIEW", PageView)