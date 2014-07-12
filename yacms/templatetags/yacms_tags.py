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
