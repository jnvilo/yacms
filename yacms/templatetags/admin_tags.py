from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template

register = template.Library()


class AdminNode(template.Node):

    #def __init__(self,values):

        #self.empty = False
        #self.template = get_template("templatetags/vertical_menu.html")
        #try:
            #self.path = values[0]

            #self.root_obj = Path.objects.get(path=self.path)
            #self.child_entries = Entry.objects.filter(path__parent=self.root_obj, path__handler="CMSContainerHandler").order_by("-path__sort_key1")

        #except IndexError as e:
            #pass

        #except ObjectDoesNotExist as e:
            #self.empty = True

    #def render(self, context):

        #if self.empty:
            ###Tell user there is no menu entry
            #result = """<li class="dropdown">"""
            #result = result +  """<a href="/">NO MENU</a>"""
            #result = result + """</li>"""
            #return result

        #request = context.get("request")
        #self.c = Context({"request":request,
                          #"root_obj":self.root_obj,
                          #"child_entries":self.child_entries})
        ##return self.template.render(self.c)
        #return self.html()
    #def html(self):

        #entry = self.root_obj.entry_obj
        #result = """<li class="dropdown">"""
        #result = result +  """<a href="{}" title="{}">{}</a>""".format(entry.get_absolute_url(), entry.title, entry.title)

        #result = result + """ <ul class="dropdown-menu">"""
        #for c in self.child_entries:
            #result = result + """<li><a href="{}" title="{}">{}</a></li>""".format(c.get_absolute_url(),c.title, c.title)
            ##process the children of each
            #gc_entries = Entry.objects.filter(path__parent=c.path, path__handler="CMSContainerHandler")
            #for each in gc_entries:
                #result = result + """<li><a href="{}" title="{}">&nbsp;-&nbsp;{}</a></li>""".format(each.get_absolute_url(),each.title, each.title)





        #result = result + "</ul>"
        #result = result + "</li>"
        #return result



#def vertical_menu(parser, token):
    #values = token.split_contents()
    #return VerticalMenuNode(values[1:])

#register.tag("vertical_menu", vertical_menu)
