from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject

from mycms.view_handlers.mycms_view import ArticleList

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


import logging
logger = logging.getLogger("mycms.page_handlers")


# #####################
# We ensure that the base page types are already created.
# #####################


#Import page_types to ensure that the page_types are created in the database.

#TODO: There should be a better way of doing this only once after startup.

from mycms.view_handlers import page_types

    
class CategoryPage(page_types.BasePage):

    def __init__(self, page_object, request=None):
        self.page_object = page_object
        self.request = request
        

    @property
    def articles(self):

        """Here we load all pages that says we are their parent."""

        from django.db.models import Q
        
       
        # ######################################################################
        # This loads up all the articles that are 
        # of type single_page or multipage and has the provided parent. 
        # 
        # We also paginate. So we need two information
        #
        # paginate_by = 10
        # page = 2
        
        limit, offset, page = self.get_list_params()
            
        
<<<<<<< HEAD
            
        try:
            obj_list = CMSEntries.objects.filter((Q(page_type = page_types.singlepageview_pagetype_obj) | Q(page_type = page_types.multipageview_pagetype_obj)) &
=======
        obj_list = CMSEntries.objects.filter((Q(page_type = page_types.singlepageview_pagetype_obj) | Q(page_type = page_types.multipageview_pagetype_obj)) &
>>>>>>> 0.1.1
                                             Q(path__parent__id = self.page_object.path.id) & Q(published=True) )[offset:offset+limit]
        except Exception as e:
            print(e)
            print(e)
            pass
        #wrap the entries of the obj_list into their view_handler representations
        obj_list_count  = CMSEntries.objects.filter((Q(page_type = page_types.singlepageview_pagetype_obj) | Q(page_type = page_types.multipageview_pagetype_obj)) &
                                             Q(path__parent__id = self.page_object.path.id) & Q(published=True) )[offset:offset+limit].count()        
        
      
        article_list = ArticleList(obj_list_count, page)        
        
        for obj in obj_list:
            article_list.append(ViewObject(page_object=obj))

        return article_list

    def get_categories(self):
        """Returns a list of all child categories of type: CATEGORY"""

        print("doping query")
        try: 
            obj_list = CMSEntries.objects.filter(path__parent__id = self.page_object.id,
                                                 page_type=self.page_object.page_type)
        except Exception as e: 
            print(e)

        print("done with the query")
        return obj_list

    
    @property
    def categories(self):
        return self.get_categories()

    def page_types(self):
        """
        Refactor me into a parent class.
        returns a list fo page_types
        """

        pagetype_objs = CMSPageTypes.objects.all()

        return pagetype_objs


    def on_create(self):
        pass

    
    def all_sub_articles(self):
        """
        Returns all articles under this category.
        """
        
        from django.db.models import Q
        
       
        
        obj_list = CMSEntries.objects.filter((Q(page_type = page_types.singlepageview_pagetype_obj) | 
                                              Q(page_type = page_types.multipageview_pagetype_obj)) &
                                             Q(path__path__startswith =  self.page_object.path.path))               
                

        return obj_list



    
    


