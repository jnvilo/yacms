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


#class Pages(models.Model):

    #path = models.ForeignKey("Paths",null=True)
    #title = models.CharField(max_length=1024)
    #slug = models.SlugField(max_length=1024)
    #content = models.TextField(max_length=20480, default="Empty")
    #date_created = models.DateTimeField(auto_now_add=True)
    #date_modified = models.DateTimeField(default=datetime.utcnow)
    #page_type = models.CharField(max_length=255, default="HTML")
    #template = models.CharField(max_length=244, default=None)
    #frontpage = models.BooleanField(default=False)
    #published = models.BooleanField(default=False)
    #meta_description = models.TextField(max_length=20480, default="")
    #article_logo = models.TextField(max_length=1023, null=True, blank=True)
    #page_number = models.IntegerField(default=1)
    
    
    #@property
    #def parent_obj(self):
        
        #path = self.page_obj.path.path
        #path = path.rstrip("/") #just to make sure no trailing / exists
        
        #try:
            #parent_path = path[:path.rindex("/")]
        #except ValueError as e:
            ##if we get here it means path was "" [i.e empty]
            #parent_path = "/"
            
        
        #parent_obj =  Pages.objects.get(path__path=parent_path)
        #return parent_obj    

    #@property
    #def parent_path(self):
        #return self.parent_obj.path.path
        
        



    #@classmethod
    #def get_or_create_from_request(self, request, 
                                   #path=None, 
                                   #title="No Title",
                                   #page_type="HTML"):

        #if not path:
            #raise AttributeError("get_or_create_from_request requires a path kwargs param")

        #path_obj, _ = Paths.objects.get_or_create(path=path)
        #pages_obj, _ = Pages.objects.get_or_create(path=path_obj,
                                                   #title=title,
                                                   #page_type=page_type)
        #return pages_obj


    #@property
    #def view(self):
        #from yacms import pageview
        #PageViewClass =  pageview.get_page_class(self.page_type)     
        #instance =  PageViewClass(self)
        #return instance
    #def save(self, *args, **kwargs):    

        #if self.slug is None or self.slug=="":
            #self.slug = slugify(self.title)

        #if self.template is None:
            #self.template = "{}.html".format(self.page_type.lower()) 
          
        
        
        #super(Pages, self).save(*args, **kwargs)
        
        ##Invalidate our caches.
        #key_name = "{0}:{1}:{2}".format("introduction",
                                        #self.path.path, 
                                        #self.title) 
        
        #key_name = key_name.replace(" ", "_")
        #cache.delete(key_name)
        
    #def response(self,request, **kwargs):    
        #return self.view.response(request, **kwargs)



    #def get_absolute_url(self):
        #"""Returns the absolute url. Prepending the YACMS_BASE_URL."""

        #path = self.path.path

        #if path.startswith("/"):
            #path = path.lstrip("/")
        #return "/{}{}".format(YACMS_BASE_URL,path)

    #def data_dict(self):

        #d = { "path": self.path_path , 
              #"title": self.title, 
              #"slug": self.slug, 
              #"date_created": self.date_created,
              #"date_modified" : self.date_modified, 
              #"page_type": self.paget_type,
              #}

    #def __str__(self):

        #return self.title


 
    #def introduction(self):
        #return self.view.introduction()
    
    
    #def logo(self):
        
        #if self.article_logo:
            #if not self.article_log.startswith("/"):
                #return "{}{}".format(YACMS_ARTICLE_LOGOS_URL, self.article_logo)
            #else:
                #return "{}{}".format(YACMS_ARTICLE_LOGOS_URL, self.article_logo)
        
        #else:
            #return None
            
class CMSPaths(models.Model):
    path = models.CharField(max_length=2000, null=True)
    parent = models.ForeignKey("CMSPaths", null=True, blank=True)
    
    def __str__(self):
        return self.path
          
class CMSTags(models.Model):
    name = models.CharField(max_length=256, default="NotSet")
    
    def __str__(self):
        return self.name
    
class CMSMarkUps(models.Model):
    markup = models.CharField(max_length=128, default="Creole")       
    
    def __str__(self):
        return self.markup
    
class CMSContents(models.Model):    
    content = models.TextField(max_length=20480, default="Empty")
    timestamp = models.DateTimeField(auto_now=True)
    markup = models.ForeignKey(CMSMarkUps, null=True)
    meta_description = models.TextField(max_length=20480, default="", blank=True)
    tags = models.ManyToManyField(CMSTags, blank=True )
    
    def __str__(self):
        return self.content

class CMSTemplates(models.Model):
    name = models.CharField(max_length=1024, default="page.html")
    template = models.TextField(max_length=10240, default="empty template")
    
    def __str__(self):
        return self.name
    
class CMSPageTypes(models.Model):
    page_type = models.CharField(max_length=64, default="DefaultType")
    text = models.CharField(max_length=128, default="default class")
    view_class = models.CharField(max_length=256, default="DefaultView")
    view_template = models.CharField(max_length=32, default=None)
    
    
    def save(self, *args, **kwargs):
        #if (self.pk is None) and (self.view_template is None):
        if (self.view_template is None):
            #We only care to put the view template as the name of the view_class
            #during the creation.
            self.view_template = "{}.html".format(self.view_class)
        
        super(CMSPageTypes, self).save(*args, **kwargs)
    

    
    
    def __str__(self):
        return self.text
    
class CMSEntries(models.Model):
    title = models.CharField(max_length=1024, default=None)
    path = models.ForeignKey(CMSPaths, null=True)
    slug = models.SlugField(max_length=1024)
    
    #We make the content a many to many to be able to handle multiple
    #so we can version by published.
    content = models.ManyToManyField(CMSContents, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    page_type = models.ForeignKey(CMSPageTypes, null=True)
    template = models.ForeignKey(CMSTemplates, null=True, blank=True)
    
    frontpage = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    page_number = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title
    

  

    
    
    