from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import pathlib
from datetime import datetime
from django.core.cache import cache

from django.db import models
from django.template.defaultfilters import slugify

from django.conf import settings

from yacms import YACMS_ARTICLE_LOGOS_URL
from yacms import YACMS_BASE_URL

class Paths(models.Model):
    path = models.CharField(max_length=1024, default="/", unique=True)
    parent = models.ForeignKey("Paths", null=True)

    def save(self, *args, **kwargs):    
        """
        We override the save so that we can ensure that if we are 
        not saving a root path, we create the parent. this happens
        recursively. 
        """

        parent_path = pathlib.Path(self.path).parent.as_posix()

        #set the parent on save to ensure we have a parent.
        if not parent_path == self.path:

            self.parent, _ = Paths.objects.get_or_create(path=parent_path)
        super(Paths, self).save(*args, **kwargs)    


    def __str__(self):

        return self.path

class Pages(models.Model):

    path = models.ForeignKey("Paths",null=True)
    title = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=1024)
    content = models.TextField(max_length=20480, default="Empty")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(default=datetime.utcnow)
    page_type = models.CharField(max_length=255, default="HTML")
    template = models.CharField(max_length=244, default=None)
    frontpage = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    meta_description = models.TextField(max_length=20480, default="")
    #article_logo = models.TextField(max_length=1023, null=True, blank=True)
    
    
    


    @classmethod
    def get_or_create_from_request(self, request, 
                                   path=None, 
                                   title="No Title",
                                   page_type="HTML"):

        if not path:
            raise AttributeError("get_or_create_from_request requires a path kwargs param")

        path_obj, _ = Paths.objects.get_or_create(path=path)
        pages_obj, _ = Pages.objects.get_or_create(path=path_obj,
                                                   title=title,
                                                   page_type=page_type)
        return pages_obj


    @property
    def view(self):
        from yacms import pageview
        PageViewClass =  pageview.get_page_class(self.page_type)     
        instance =  PageViewClass(self)
        return instance
    def save(self, *args, **kwargs):    

        if self.slug is None or self.slug=="":
            self.slug = slugify(self.title)

        if self.template is None:
            self.template = "{}.html".format(self.page_type.lower()) 
          
        
        
        super(Pages, self).save(*args, **kwargs)
        
        #Invalidate our caches.
        key_name = "{0}:{1}:{2}".format("introduction",
                                        self.path.path, 
                                        self.title) 
        
        key_name = key_name.replace(" ", "_")
        cache.delete(key_name)
        
    def response(self,request, **kwargs):    
        return self.view.response(request, **kwargs)



    def get_absolute_url(self):
        """Returns the absolute url. Prepending the YACMS_BASE_URL."""

        path = self.path.path

        if path.startswith("/"):
            path = path.lstrip("/")
        return "/{}{}".format(YACMS_BASE_URL,path)

    def data_dict(self):

        d = { "path": self.path_path , 
              "title": self.title, 
              "slug": self.slug, 
              "date_created": self.date_created,
              "date_modified" : self.date_modified, 
              "page_type": self.paget_type,
              }

    def __str__(self):

        return self.title


 
    def introduction(self):
        return self.view.introduction()
    
    
    def logo(self):
        
        if self.article_logo:
            if not self.article_log.startswith("/"):
                return "{}{}".format(YACMS_ARTICLE_LOGOS_URL, self.article_logo)
            else:
                return "{}{}".format(YACMS_ARTICLE_LOGOS_URL, self.article_logo)
        
        else:
            return None
                
                
            
            
            
