from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template


#from yacms.models import Paths, Pages
#from yacms.pageview.base import get_pageview

from yacms.models import  CMSPaths
from yacms.models import CMSEntries

register = template.Library()


@register.inclusion_tag('yacms/templatetags/frontpage.html')
def frontpage():
    cmsentries = CMSEntries.objects.filter(frontpage=True, published=True).order_by("-date_created")[:10]

    for cmsentry in cmsentries:
        print(cmsentry)
    return {"cmsentries":cmsentries}







