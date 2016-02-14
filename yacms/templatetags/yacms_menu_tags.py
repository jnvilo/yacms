from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template


#from yacms.models import Paths, Pages
#from yacms.pageview.base import get_pageview

from yacms.models import  CMSPaths
from yacms.models import CMSEntries

register = template.Library()

@register.inclusion_tag('yacms/templatetags/dropdown_menu.html')
def dropdown_menu(path):
    
    
    parent = CMSEntries.objects.get(path__path=path)
    
    for each in parent.categories():
        print(each)
        
    
    return {"parent":parent}


