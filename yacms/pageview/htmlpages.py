from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from creole import creole2html
from random import randrange
import loremipsum
import arrow
import re

from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.template.defaultfilters import slugify

from django.core.cache import cache
from yacms.models import Pages

from .base import BaseView
from .base import register
from .creole_macros import code
from .creole_macros import pre
from .creole_macros import HTML
from .creole_macros import image

class PageView(BaseView):
    
    def html(self):
        """This parses the content using creole."""
        
        
        content = self.page_obj.content
        html_str = creole2html(content, debug=False, parser_kwargs={}, 
                   emitter_kwargs={}, block_rules=None, 
                    blog_line_breaks=True, macros={ "code": code, 
                                                   "pre": pre,
                                                   "HTML": HTML,
                                                   "image": image}, 
                   verbose=None,  stderr=None)
        
        #now parse for the "__DOCUMENT_URL_REGEX_REPLACED__
        #to replace it with our url path. 
        
        page_path = self.page_obj.path.path
        
        if page_path.startswith("/"):
            page_path = page_path.lstrip("/")
        
        path = "/assets/{}".format(page_path)
      
        result =  re.sub("__DOCUMENT_URL_REGEX_REPLACED__", path, html_str)        
        return result
    
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
            
                if meta_header:
                    page_obj.meta_description = meta_header
            
                page_obj.save()
                self.page_obj = page_obj
                
                
                return JsonResponse(data={"message": "Successfully Saved data."})
                
        #if action is not None:  
        #    return JsonResponse(data={"error_msg": "action: {} not supported.".format(action)})    
            
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
        
        
        
        

register("HTMLVIEW", PageView, "Single Page HTML")


class MultiPageView(PageView):
    
    @property
    def is_home_page(self):
        if self.page_obj.page_type == "MULTIPAGEINDEX":
            return True
        else:
            return False
        
    @property
    def is_member_page(self):
        if self.page_obj.page_type == "MULTIPAGEENTRY":
            return True
        else:
            return False
        
    def bookmarks(self):
    
        lines = self.html().split("\n")
        
        url_list = []
        for line in lines:
            match_obj = re.match("""<a name=.*><h2>(?P<text>.*)</h2></a>""", line)
                
            if match_obj:
                text = match_obj.group("text")
                slug = slugify(text)
                url_list.append({ "slug": slug, "text":text})
                
        return url_list
        
                    
                    
                    
            
    def _update_h2_bookmarks(self, html):
        
        lines = html.split('\n')
        
        updated_lines = []
        for line in lines:
            match_obj = re.match("^<h2>(?P<text>.*)</h2>$", line)
        
            if match_obj:
                text = match_obj.group("text")
                slug = slugify(text)
                line = """<a name="{}"><h2>{}</h2></a>""".format(slug, text) 
                
            else:
                line
            
            updated_lines.append(line)
            
        return ("\n").join(updated_lines)
            
    def html(self):
            """This parses the content using creole. It also updates the 
            page to replace all of the h2 with bookmarks."""
            
            
            #First step: Turn the content into HTML
            content = self.page_obj.content
            html_str = creole2html(content, debug=False, parser_kwargs={}, 
                       emitter_kwargs={}, block_rules=None, 
                        blog_line_breaks=True, macros={ "code": code, 
                                                       "pre": pre,
                                                       "HTML": HTML,
                                                       "image": image}, 
                       verbose=None,  stderr=None)
            
            #now parse for the "__DOCUMENT_URL_REGEX_REPLACED__
            #to replace it with our url path. The image macro creates this.
            
            page_path = self.page_obj.path.path
            
            if page_path.startswith("/"):
                page_path = page_path.lstrip("/")
            
            path = "/assets/{}".format(page_path)
          
            result =  re.sub("__DOCUMENT_URL_REGEX_REPLACED__", path, html_str)        
            
            #Now find all <h2></h2> and update them
            
            
            return self._update_h2_bookmarks(result)        
  
  
    def navigation(self):
        
        count = 0 
        num_entries = self.member_objs.count()
        
        if self.is_home_page:
            members_list = [self.page_obj]
            home_pageview = self
        else:
            #get the parent then.
            members_list = [self.parent_obj]
            home_pageview = self.parent_obj.view
        
        #members_list = list(self.member_objs)
        for each in self.member_objs:
            members_list.append(each)
            
        
        
        for each in members_list:
            if each.pk == self.page_obj.pk:
                index = count
                break
            count = count + 1
            
        if index==0:
            #we are the first page
            prev_pageview = None
            
            try:
                next_pageview = (members_list[1]).view
            except IndexError:
                #we do not have members
                next_pageview = None
                
        elif index==num_entries:
            #we are at the end
            prev_pageview = (members_list[index -1]).view
            next_pageview = None
            
        else:
            #We are somewhere in the middle
            prev_pageview = (members_list[index - 1]).view
            next_pageview = (members_list[index + 1]).view
            
        return { "previous": prev_pageview,"next": next_pageview,
                 "home": home_pageview}
            
            
            
        
    @property
    def member_objs(self):
        raise NotImplementedE("Inheriting class must implement me!")


class MultiPageIndexView(MultiPageView):
    
    @property
    def member_objs(self):
        return Pages.objects.filter(path__parent=self.path_obj, 
                                    page_type="MULTIPAGEENTRY").order_by("date_created")        
        
   
    def iter_members_pageviews(self):
        
        yield self.view
        for each in self.member_objs:
            yield each.view  
       
register("MULTIPAGEINDEX", MultiPageIndexView, "Multiple Pages Article", template="multipage.html")

class MultiPageEntryView(MultiPageView):
    
    @property
    def member_objs(self):
        return Pages.objects.filter(path__parent=self.parentview.path_obj, 
                                    page_type="MULTIPAGEENTRY").order_by("date_created")        
     
    
    def iter_members_pageviews(self): 
        
        yield self.parentview
        for each in self.member_objs:
            yield each.view   
            


register("MULTIPAGEENTRY", MultiPageEntryView, None, template="multipage.html")


