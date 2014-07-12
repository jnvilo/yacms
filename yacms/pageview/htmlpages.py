from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from creole import creole2html
from random import randrange
import loremipsum

from bs4 import BeautifulSoup
from django.http import JsonResponse

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
        
        return super(PageView, self).exec_action(request, **kwargs)


    
    def introduction(self):
        
        html = self.html()
        
        soup = BeautifulSoup(html)
        
        p = soup.find("p")
        
        s = str(p)
        s = s.lstrip("<p>")
        s = s.rstrip("</p>")
        
        return s
        
        
        
        

register("HTMLVIEW", PageView)