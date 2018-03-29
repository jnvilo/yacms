from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.paginator import Paginator


from django.template.loader import render_to_string

#from yacms.models import Paths, Pages
#from yacms.pageview.base import get_pageview

from yacms.models import  CMSPaths
from yacms.models import CMSEntries

register = template.Library()

 

@register.inclusion_tag('yacms/templatetags/frontpage.html')
def frontpage():
    
    
    cmsentries = CMSEntries.objects.filter(frontpage=True, published=True).order_by("-date_created")
    paginator = Paginator(cmsentries, 4)
    
    return {"cmsentries":cmsentries}









