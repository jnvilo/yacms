from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template

from yacms.models import Paths, Pages
from django.forms.models import model_to_dict
register = template.Library()


class ModelAttributesNode(template.Node):

    def __init__(self,path_str):

        self.empty = False
        self.template = get_template("yacms/tags/model_attributes.html")
        try:

            path_obj = Paths.objects.get(path=path_str)
            page_obj = Pages.objects.get(path=path_obj)
            self.page_obj = page_obj
            
            
        except ObjectDoesNotExist as e:
            self.page_obj = None


    def render(self, context):
        
        request = context.get("request")
        
        model_dict = model_to_dict(self.page_obj)
        
        attribute_list = []
        #Now we create a value_name list to display
        for key in model_dict.keys():
            attribute_list.append({ "name": key, "value": model_dict[key]})
        
        
        self.c = Context({"request":request,
                          "pageview": self.pageview,
                          "model_attributes": attribute_list,
                        })
        
        return self.template.render(self.c)
        
def model_attributes(parser, token):
    values = token.split_contents()
    return ModelAttributesNode(values[1:])

register.tag("model_attributes", model_attributes)
