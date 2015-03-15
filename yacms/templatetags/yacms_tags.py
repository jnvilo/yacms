from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template

from yacms.models import CMSEntries
register = template.Library()

import logging
logger = logging.getLogger("yacms.template_tags")
class FrontPageArticles(template.Node):
    
    def render(self, context):
        
        cmsentry_objs = CMSEntries.objects.filter(frontpage = True, published=True)
        #package each of the content into a YACMSViewObject
        
        if cmsentry_objs.count() == 0:
            logger.debug("Warning: Found 0 FrontPage objects.")
        
        view_list = []
        for each in cmsentry_objs:
            view_list.append(each.view)
        
        context["frontpage_entries"] = view_list
        return ''
        
def get_frontpage_entries(parser, token):
    
    #values = token.split_contents()
    return FrontPageArticles()

register.tag("get_frontpage_entries", get_frontpage_entries)
        

class VerticalCollapsedCategoryMenuNodes(template.Node):
    
    def __init__(self):
        self.path = "/"
        
    def render(self, context):
        
        html = """<select id="menu" name="menu">"""
        html += """ <option value="/">Home</option>"""        
        try:
            obj = CMSEntries.objects.get(path__path = self.path)
            obj_list = CMSEntries.objects.filter(path__parent__path=self.path, page_type__page_type="CATEGORY")
        
           
            
            for obj in obj_list:
                html += """ <option value="/cms{}">{}</option>""".format(obj.path.path, obj.title)
                
                #Get the children as well
                child_obj_list = CMSEntries.objects.filter(path__parent=obj.path, page_type__page_type="CATEGORY")
                for child_obj in child_obj_list:
                    html += """ <option value="/cms{}">&nbsp; - &nbsp;{}</option>""".format(child_obj.path.path, child_obj.title)      
                
                
                
           
          
        except ObjectDoesNotExist as e:
        
            msg = "Failed to load CMSENTRY: {} while constructing VerticalCollapsedCategoryMenuNodes".format(self.path)
            logger.debug(msg)
            
            html +=  """ <option value="">Failed to load: {}</option>""".format(self.path)                

            
        html += "</select><!--generated -->"  
        return html
 
def vertical_collapsed_menu_bar(parser, token):
   
    return VerticalCollapsedCategoryMenuNodes()
            
register.tag("vertical_collapsed_menu_bar", vertical_collapsed_menu_bar)

       

        
        
class VerticalCategoryMenuNodes(template.Node):
    
    def __init__(self, path):
        self.path = path
        
    def render(self, context):
        
        html = """<!--generated --><ul class="nav nav-list">"""
        try:
            obj = CMSEntries.objects.get(path__path = self.path)
            obj_list = CMSEntries.objects.filter(path__parent__path=self.path, page_type__page_type="CATEGORY")
            
           
            html += """<li class="nav-header"><a href="/cms/{}">{}</a></li>""".format(obj.path,obj.title)
            
            for obj in obj_list:
                html += """<li><a href="/cms{}" title>{}</a></li>""".format(obj.path.path, obj.title)
                
                #Get the children as well
                child_obj_list = CMSEntries.objects.filter(path__parent=obj.path, page_type__page_type="CATEGORY")
                for child_obj in child_obj_list:
                    html += """<li><a href="/cms{}" title>&nbsp; - &nbsp;{}</a></li>""".format(child_obj.path.path, child_obj.title)            
                
                
                
           
        except ObjectDoesNotExist as e:
            
            html += "<li>Failed to load: {}</li>".format(self.path)
            
            msg = "Failed to load CMSEntry while building VerticalCategoryMenuNodes for path: {} ".format(self.path)
            logger.debug("")
            
        html += "</ul><!--generated -->"
        return html
 
def vertical_menu_bar(parser, token):
    values = token.split_contents()
    params = values[1:]
    return VerticalCategoryMenuNodes(params[0])
            
register.tag("vertical_menu_bar", vertical_menu_bar)

       


class CategoryMenuBar(template.Node):
    
    def __init__(self, params):
        self.params = params
    
    def render(self, contenxt):
        
        if len(self.params) == 0:
            return "category_menu_bar requires a string containt space separated slugs of category names."
        else:
            return self.html(self.params)
    
    def get_dropdown_menu(self, cmsentry_object):
        
        path_obj = cmsentry_object.path
        obj_list = CMSEntries.objects.filter(path__parent = path_obj, page_type__page_type="CATEGORY")
        result = """<ul class="dropdown-menu">"""
        if len(obj_list) == 0:
            return None
        
        else:
            
            for obj in obj_list:
                result += """<li><a href="/cms{}" title>{}</a></li>""".format(obj.path.path, obj.title)
                second_level_result = self.get_second_level_children(obj)
                
                if second_level_result:
                    result += second_level_result
                
            result += "</ul>"
                
            return result
                
    def get_second_level_children(self, cmsentry_object):
        
        path_obj = cmsentry_object.path
        obj_list = CMSEntries.objects.filter(path__parent = path_obj, page_type__page_type="CATEGORY")
        result = ""
        if len(obj_list) == 0:
            return None
        else:
            for obj in obj_list:
                result += """<li ><a href="/cms{}" title>&nbsp;&nbsp;{}</a></li>""".format(obj.path.path, obj.title)    
            return result        
        
    def html(self, params):

        #Build a datastructure that holds our menua
        menu_dict = { }
        
        result = ""
        for each in params:
            if not each.startswith("/"):
                each = "/" + each
               
            try: 
                cmsentry_obj = CMSEntries.objects.get(path__path=each)
                result += """<li class="dropdown">"""
                #Do we have children? 
                result += """ <a href="/cms{}">{}</a> """.format(cmsentry_obj.path.path, cmsentry_obj.title)
                child_menu = self.get_dropdown_menu(cmsentry_obj)
                
                if child_menu:
                    result += child_menu
                
                result += "</li>"
            
            except ObjectDoesNotExist as e:
                
                
                result += """<li class="dropdown">"""
                result += """ <a href="">{}NotFound</a> """.format(each.upper().lstrip("/"))
                result += "</li>"
            
        return result
        

def category_menu_bar(parser, token):
    
    values = token.split_contents()
    params = values[1:]
    return CategoryMenuBar(params)
    
register.tag("category_menu_bar", category_menu_bar)


class BreadCrumbs(template.Node):
   
        
    def render(self, context):

        try:
            view_object = context["view_object"]
        except KeyError as e:
            return ''
        path = view_object.page_object.path.path
        entries_list = []
    
        while 1:
            path = path[:path.rfind("/")]
            if path == '':
                break
            cmsentry_obj = CMSEntries.objects.get(path__path = path)
            entries_list.append(cmsentry_obj)
        
        entries_list.reverse()
        
        result_list = []
        
        for entry in entries_list:
            r = { "path": "/cms" + entry.path.path, "text": entry.title }
            result_list.append(r)
        
        context['breadcrumbs'] = result_list
        
        
        return ''
    
def get_breadcrumbs(parser, token):
        
    values = token.split_contents()
  
    return BreadCrumbs()
register.tag("get_breadcrumbs", get_breadcrumbs)