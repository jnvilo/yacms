from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template
import re

#from mycms.models import Paths, Pages
#from mycms.pageview.base import get_pageview


register = template.Library()
from . import registry

script_str_re_obj =re.compile(r"""(?P<name>src|type)="(?P<value>.*)"|((?P<name2>priority)=(?P<value2>(\d*)))""", re.DOTALL)


@register.inclusion_tag('mycms/templatetags/file_upload.html')
def file_upload():
    #Nothing to add to the context for now.
    return { "none": None }

@register.inclusion_tag('mycms/templatetags/article_editor.html')
def article_editor():
    #Nothing to add to the context for now.
    return { "none": None }




class NullNode(template.Node):
    
    def __init__(self):
        pass
    
    def render(self, context):
        return ""

class ScriptEntry(object):
    
    def __init__(self, src, script_type, priority):
        self.src = src
        self.script_type = script_type
        self.priority = priority
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def __eq__(self, other):
        return self.priority == other.priority
    
    def __str__(self):
        
        return """<script src="{}"></script>  """.format(self.src)

@register.simple_tag(takes_context=True)
def Script(context, *args, **kwargs):
    
    script_list = context.get("script_list", None)
    if not script_list:
        script_list = []
        context["script_list"] = script_list
     
    if kwargs.get("src") is not None:
        
        context["script_list"].append(ScriptEntry(src=kwargs.get("src","/dummy/path"),
                                        script_type=kwargs.get("type", "text/javascript"),
                                        priority=kwargs.get("priority", 9999)))
    #print(context["script_list"])
    print("script_list: {}".format(len(script_list)))
    print("Adding {}".format(kwargs.get("src")))   
    return ""
        
@register.simple_tag(takes_context=True)
def CollectedScripts(context, *args, **kwargs):
    
    
    result_str = ""
    script_list = context.get("script_list",None)
    if script_list:
        for script in context["script_list"]:
            result_str += "{}\n".format(str(script))
        return result_str  
    else:
        return """<!-- no scripts to display>"""
    
    
class ScriptCollectorNode(template.Node):
    def __init__(self):
        
        pass

    def __repr__(self):
        return "<ScriptCollectorNode>"

    def render(self, context):
       
        self.request = template.Variable('request')
        j = self.request.jason
        
        return registry.html()
    
@register.tag
def ScriptCollector(parser, token_str):
    return ScriptCollectorNode()

    
class NullNode(template.Node):
    
    def __init__(self):
        pass
    
    def render(self, context):
        return ""


@register.tag
def Link(parser, token_str):
    """
    Adds a <link> for our css at the header of the page.   
    """
 
    def parse_tokens(tokens):
        
        tokens = token_str.split_contents()
        tokens = tokens[1:] #the first is always the tag name.        
    
        #each token is expected to be of the format 
        # name=value


    
    
    
    