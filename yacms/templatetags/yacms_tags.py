from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template

from yacms.models import Paths, Pages
register = template.Library()


class FrontPageNode(template.Node):

    def __init__(self,values):

        self.empty = False
        self.template = get_template("yacms/tags/frontpage_pages.html")
        try:

            path_obj = Paths.objects.get(path="/")
            page_obj = Pages.objects.get(path=path_obj)
            
            self.pageview = page_obj.view
            
        except ObjectDoesNotExist as e:
            self.pageview = None


    def render(self, context):
        request = context.get("request")
        self.c = Context({"request":request,
                          "pageview": self.pageview,
                        })
        return self.template.render(self.c)
        
def frontpage_pages(parser, token):
    values = token.split_contents()
    return FrontPageNode(values[1:])

register.tag("frontpage_pages", frontpage_pages)


class ContentEditorNode(template.Node):
    
    def __init__(self):
        template_name = "yacms/tags/content_editor_node.html"
        self.template = get_template(template_name)
  
        
    
    def render(self, context):  
        request = context.get("request")
        pageview = context.get("pageview")
        self.c = Context({"request":request,
                          "pageview":pageview,
                          })        
        return self.template.render(self.c)
    
def content_editor_node(parser,token):
    return ContentEditorNode()

register.tag("content_editor_node", content_editor_node)


class MetaEditorNode(template.Node):
    
    def __init__(self):
        template_name = "yacms/tags/meta_editor_node.html"
        self.template = get_template(template_name)
  
    def render(self, context):  
        request = context.get("request")
        pageview = context.get("pageview")
        self.c = Context({"request":request,
                          "pageview":pageview,
                          })        
        return self.template.render(self.c)
    
def meta_editor_node(parser,token):
    return MetaEditorNode()

register.tag("meta_editor_node", meta_editor_node)

class ImageUploaderNode(template.Node):
    
    def __init__(self):
        template_name = "yacms/tags/image_uploader_node.html"
        self.template = get_template(template_name)
  
    def render(self, context):  
        request = context.get("request")
        pageview = context.get("pageview")
        self.c = Context({"request":request,
                          "pageview":pageview,
                          })        
        return self.template.render(self.c)
    
def image_uploader_node(parser,token):
    return ImageUploaderNode()

register.tag("image_uploader_node", image_uploader_node)



class MemberPagesAdminNode(template.Node):
    
    def __init__(self):
        template_name = "yacms/tags/member_pages_admin.html"
        self.template = get_template(template_name)
  
    def render(self, context):  
        request = context.get("request")
        pageview = context.get("pageview")
        self.c = Context({"request":request,
                          "pageview":pageview,
                          })        
        return self.template.render(self.c)
    
def member_pages_admin_node(parser,token):
    return MemberPagesAdminNode()

register.tag("member_pages_admin_node", member_pages_admin_node)


class PageTagEditorNode(template.Node):
    
    def __init__(self):
        template_name = "yacms/tags/member_pages_admin.html"
        self.template = get_template(template_name)
  
    def render(self, context):  
        request = context.get("request")
        pageview = context.get("pageview")
        self.c = Context({"request":request,
                          "pageview":pageview,
                          })        
        return self.template.render(self.c)
    
def page_tag_editor_node(parser,token):
    return MemberPagesAdminNode()

register.tag("member_pages_admin_node", member_pages_admin_node)