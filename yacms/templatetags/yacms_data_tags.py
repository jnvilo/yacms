from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template

from yacms.models import Paths, Pages
register = template.Library()


def get_child_pages(context, page_type):
    
    parent_page_obj = context["page"]
    parent_path_obj = parent_page.path
    
    pages = Pages.objects.filter(path=parent_path_obj)

    return None

    