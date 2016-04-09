import logging

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template


#from yacms.models import Paths, Pages
#from yacms.pageview.base import get_pageview

from yacms.models import  CMSPaths
from yacms.models import CMSEntries

register = template.Library()

logger = logging.getLogger("yacms.templatetags")


@register.inclusion_tag('yacms/templatetags/dropdown_menu.html')
def dropdown_menu(path):

    try:
        parent = CMSEntries.objects.get(path__path=path)
    except ObjectDoesNotExist as e:
        msg = "No CMSEntries to produce dropdown_menu for path: {}".format(path)
        logger.fatal(msg)
        parent = []
    return {"parent":parent}

@register.inclusion_tag('yacms/templatetags/full_menu.html')
def full_menu():
    try:
        parent = CMSEntries.objects.get(path__path="/")
    except ObjectDoesNotExist as e:
        msg = "No CMSEntries to produce full_menu from /. Perhaps / does not yet exist!!"
        logger.fatal(msg)
        parent = None
    return {"parent":parent}










