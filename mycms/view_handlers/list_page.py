from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject

from mycms.view_handlers.mycms_view import ArticleList

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


import logging
logger = logging.getLogger("mycms.page_handlers")


"""
List Items have a main page to show lists 
and then it has 

ListPageItems

These is an extension of CMSEntries 
ListPage is a CMSEntry of Type LISTPAGE
"""



from mycms.view_handlers import page_types

class ListPage(page_types.BasePage):
    
    page_type = "LISTPAGE"
    
    def __init__(self, page_object, request=None):
        
        #The page_object in this case is the cmsentry model instance.
        self.page_object = page_object
        self.request = request
      
    @property 
    def items(self):
        """
        Returns the list items for the page.
        """
        
        page_cmsentries  = CMSEntries.objects.filter((Q(page_type = page_types.list_items_pagetype_obj) &
                                                      Q(path__parent__id = self.page_object.path.id) & 
                                                      Q(published=True) & 
                                                      Q(lists_include=True) 
                                                      )[offset:offset+limit]
                                                     )
        
        


class ListItem(page_types.BasePage):
    
    pass