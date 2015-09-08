from yacms.models import CMSEntries
from yacms.models import CMSPageTypes
from .yacms_view import YACMSViewObject

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import logging
logger = logging.getLogger("yacms.page_handlers")


try:
    singlepageview_pagetype_obj, c = obj = CMSPageTypes.objects.get_or_create( page_type = "SINGLEPAGE")
   
except ObjectDoesNotExist as e:
    singlepageview_pagetype_obj = CMSPageTypes( page_type = "SINGLEPAGE", 
                                                 text = "Single Page HTML",
                                                 view_class = "SinglePage",
                                                 view_template = "SinglePage.html")
    singlepageview_pagetype_obj.save()
   
except MultipleObjectsReturned as e:
    msg = "Got more than 1 CMSPageTypes : SINGLEPAGE. Database is inconsistent, Will return the first one. "
    logger.warn(msg)
    
    singlepageview_pagetype_obj = CMSPageTypes.objects.filter(page_type="SINGLEPAGE")[0]
   
   
try:
    categorypageview_pagetype_obj = CMSPageTypes.objects.get(page_type="CATEGORY")

except ObjectDoesNotExist as e:
    
    msg = "Could not load CATEGORY view object. Going to create it."
    logger.debug(msg)
    pagetype_obj, _ = CMSPageTypes.objects.get_or_create(page_type="CATEGORY",
                                                     text = "Category Page",
                                                     view_class = "CategoryPage",
                                                     view_template = "CategoryPage.html"
                                                     )
    
except MultipleObjectsReturned as e:
    msg = "Got more than 1 CMSPageType: CATEGORY. Database is inconsistent. Will return the first one."
    logger.info(msg)
    
    categorypageview_pagetype_obj = CMSPageTypes.objects.filter(page_type="CATEGORY")[0]

    




class CategoryPage(object):
    
    def __init__(self, page_object):
        self.page_object = page_object
        
        
    def articles(self):
        
        """Here we load all pages that says we are their parent."""
        
        obj_list = CMSEntries.objects.filter(page_type = singlepageview_pagetype_obj,
                                             path__parent__id = self.page_object.path.id)
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

    
    
    def page_types(self):
        
        """
        Refactor me into a parent class. 
        returns a list fo page_types 
        """
        
        
        pagetype_objs = CMSPageTypes.objects.all()
        
        return pagetype_objs