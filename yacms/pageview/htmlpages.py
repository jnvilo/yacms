from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from creole import creole2html
from random import randrange
import loremipsum
import arrow

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
                time_submitted = request.POST.get("json_time_submitted", None)
                date_modified = request.POST.get("json_date_modified", None)
                time_modified = request.POST.get("json_time_modified", None)
                meta_header = request.POST.get("json_meta_header", None)
                
                page_obj = self.page_obj
                
                
                if page_header_title:
                    self.page_obj.page_header_title = page_header_title
                    self.page_obj.meta_header = meta_header
               
                if date_modified:
                
                    if time_modified is None:
                        time_modified = "20:00"
                    
                    if len(time_modified) <=4:
                        time_modified = "0{}".format(time_modified)
                    
                        
                    datetime_str = "{} {}".format(date_modified, time_modified)
                    a_date = arrow.get(datetime_str, 'YYYY-MM-DD HH:mm')
                    page_obj.date_modified = a_date.datetime
                
                if date_submitted:
                                    
                    if time_submitted is None:
                        time_submitted = "20:00"
                                        
                    if len(time_submitted) <=4:
                        time_submitted = "0{}".format(time_submitted)
                                            
                    datetime_str = "{} {}".format(date_submitted, time_submitted)
                    a_date = arrow.get(datetime_str, 'YYYY-MM-DD HH:mm')
                    page_obj.date_created = a_date.datetime                
            
            
                page_obj.save()
                self.page_obj = page_obj
                
                return JsonResponse(data={"message": "Successfully Saved data."})
                
            
                
            
        return super(PageView, self).exec_action(request, **kwargs)


    
    def introduction(self):
        
        path = self.page_obj.path.path
        title = self.page_obj.title
        
        key_name = "{0}:{1}:{2}".format("introduction",path, title)  
        key_name = key_name.replace(" ", "_")
        value = cache.get(key_name)
        
        if value is None:
    
            html = self.html()
            
            soup = BeautifulSoup(html)
            
            p = soup.find("p")
            
            value = str(p)
            value = value.lstrip("<p>")
            value = value.rstrip("</p>")
            
            cache.set(key_name, value)
            
        return value
        
        
        
        

register("HTMLVIEW", PageView)