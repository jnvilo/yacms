from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template

from yacms.models import Paths, Pages
register = template.Library()


class VerticalMenuNode(template.Node):

    def __init__(self,values):

        self.empty = False
        self.template = get_template("yacms/tags/vertical_menu.html")
        try:
            self.path = values[0]

            self.root_path_obj = Paths.objects.get(path=self.path)
            self.page = Pages.objects.get(path=self.root_path_obj)
            self.child_pages = Pages.objects.filter(path__parent=self.root_path_obj, 
                                                    page_type="CATEGORYVIEW")

        except IndexError as e:
            pass

        except ObjectDoesNotExist as e:
            self.empty = True


    
    def html(self):

        page = self.page
        pages = self.child_pages
        
        
        result = """<li class="dropdown">"""
        
        result = result +  """<a href="{}" title="{}">{}</a>""".format(page.get_absolute_url(), page.title, page.title)
        result = result + """ <ul class="dropdown-menu">"""
        
        for page in self.child_pages:
            result = result + """<li><a href="{}" title="{}">{}</a></li>""".format(page.get_absolute_url(),page.title, page.title)
            #process the children of each
            grand_child_pages = Pages.objects.filter(path__parent=page.path, page_type="CATEGORYVIEW")
            for gc_page in grand_child_pages:
                result = result + """<li><a href="{}" title="{}">&nbsp;-&nbsp;{}</a></li>""".format(gc_page.get_absolute_url(),
                                                                                                    gc_page.title, 
                                                                                                    gc_page.title)

        result = result + "</ul>"
        result = result + "</li>"
        return result

    def render(self, context):

        if self.empty:
            ##Tell user there is no menu entry
            result = """<li class="dropdown">"""
            result = result +  """<a href="/">NO MENU</a>"""
            result = result + """</li>"""
            return result

        #request = context.get("request")
        #self.c = Context({"request":request,
        #                  "roo_obj":self.root_obj,
        #                  "child_entries":self.child_entries})
        #return self.template.render(self.c)
        return self.html()
    
def vertical_menu(parser, token):
    values = token.split_contents()
    return VerticalMenuNode(values[1:])

register.tag("vertical_menu", vertical_menu)
