from yacms.models import CMSEntries
from yacms.models import CMSPageTypes
from .yacms_view import YACMSViewObject
singlepageview_pagetype_obj = CMSPageTypes.objects.get(page_type="SINGLEPAGE")

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

    
    
    