from yacms.models import CMSEntries
from yacms.models import CMSPageTypes
from .yacms_view import YACMSViewObject

from django.core.exceptions import ObjectDoesNotExist

import logging
logger = logging.getLogger("yacms.page_handlers")


try:
    singlepageview_pagetype_obj = CMSPageTypes.objects.get(page_type="SINGLEPAGE")
except ObjectDoesNotExist as e:
    
    msg = "Could not load SINGLEPAGE view object. Going to create it."
    logger.debug(msg)
    
    obj = CMSPageTypes()
    obj.page_type = "SINGLEPAGE"
    obj.text = "Single Page HTML"
    obj.view_class = "SinglePage"
    obj.view_template = "SinglePage.html"
    obj.save()
    
    singlepageview_pagetype_obj = obj


try:
    categorypageview_pagetype_obj = CMSPageTypes.objects.get(page_type="CATEGORYPAGE")
except ObjectDoesNotExist as e:
    
    msg = "Could not load CATEGORY view object. Going to create it."
    logger.debug(msg)
    
    obj = CMSPageTypes()
    obj.page_type = "CATEGORY"
    obj.text = "Category Page"
    obj.view_class = "CategoryPage"
    obj.view_template = "CategoryPage.html"
    obj.save()
    categorypageview_pagetype_obj = obj






class CategoryPage(object):
    
    def __init__(self, page_object):
        self.page_object = page_object
        
        
    def articles(self):
        #SINGLEPAGEVIEW
        obj_list = CMSEntries.objects.filter(path__parent_id = self.page_object.id,
                                  page_type = singlepageview_pagetype_obj)
        
        #wrap the entries of the obj_list into their view_handler representations
        view_list = []
        for obj in obj_list:
            view_list.append(YACMSViewObject(page_object=obj))
            
        return view_list
            
        
        
    def get_categories(self):  
        """Returns a list of all child categories of type: CATEGORY"""
        
        obj_list = CMSEntries.objects.filter(path__path__parent__id = self.page_object.id,
                                             page_type=page_obj.page_type)
        
        return obj_list

    
    
    