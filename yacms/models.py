from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from django.db.models.signals import post_save

import pathlib
from datetime import datetime
from django.core.cache import cache

from django.db import models
from django.template.defaultfilters import slugify

from django.conf import settings
from yacms.creole import creole2html


from loremipsum import generate_paragraphs

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

    @property
    def html(self):




        from yacms.view_handlers.formatters import CreoleFormatter
        return CreoleFormatter(self.content).html()

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
            self.view_template = "DefaultView.html"

        super(CMSPageTypes, self).save(*args, **kwargs)




    def __str__(self):
        return self.text

class CMSEntries(models.Model):
    title = models.CharField(max_length=1024, default=None)
    path = models.ForeignKey(CMSPaths, null=True)
    slug = models.SlugField(max_length=1024, unique=True)

    #We make the content a many to many to be able to handle multiple
    #so we can version by published.
    content = models.ManyToManyField(CMSContents, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    page_type = models.ForeignKey("CMSPageTypes", null=True)
    template = models.ForeignKey(CMSTemplates, null=True, blank=True)

    frontpage = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    page_number = models.IntegerField(default=1)



    def parent(self):

        #Get the cms entry that has a path belonging to the parent of our path.
        parent_entry = CMSEntries.objects.get(path=self.path.parent)
        return parent_entry


    def __str__(self):
        return self.title


    #----------------------------------------------------------------------
    def  date_created_str(self):
        """"""
        return self.date_created.strftime("%d/%m/%Y %H:%M:%S")

    @property
    def view(self):
        from yacms.view_handlers import YACMSViewObject
        return YACMSViewObject(page_object=self)


    def get_absolute_url(self):
        cms_base_path = getattr(settings, "YACMS_BASEPATH", None)

        if not cms_base_path:
            cms_base_path = "/cms"

        if not cms_base_path.endswith("/"):
            cms_base_path = cms_base_path.rstrip("/")

        #we assume here that self.path.path will always start with a /
        return "{}{}".format(cms_base_path, self.path.path)


    def get_parent_paths(self,path_str):

        x = path_str.rfind("/")

        if x == 0 :
            #we are at the root
            return [path_str]

        else:
            return  self.get_parent_paths(path_str[:x]) + [path_str]



    def parents_list(self):

        path_str = self.path.path

        p = self.get_parent_paths(path_str)

        pl = []
        for path_str in p:

            pl.append(CMSEntries.objects.get(path__path=path_str))

        return pl



    def categories(self):

        c = CMSEntries.objects.filter(path__parent=self.path, page_type__page_type="CATEGORY")
        return c

    #def save(self, *args, **kwargs):

        #if self.pk is None:
            #tell parent to save ourselves so we get a pk.
            #super(CMSEntries, self).save(*args, **kwargs)

            #print("WE HAVE A PK: {} ".format(self.pk))
            ##This is a new cms entry
            ##create a new content and
            #paragraphs = generate_paragraphs(5, start_with_lorem=False)
            #p = ""
            #for paragraph in paragraphs:
                #p =  unicode(paragraph[2]) + "\n\n" + p
            #h =  creole2html(p)

            #obj = CMSContents()
            #obj.content = "This is a new content."
            #obj.save()

            #cms_obj = CMSEntries.objects.get(id=self.pk)
            #cms_obj.content.add(obj)


        #else:
            #super(CMSEntries, self).save(*args, **kwargs)


## method for updating
#def create_default_content(sender, instance, created, **kwargs):

    #if created:
        #obj = CMSContents()
        #obj.content = "This is the latest content1"
        #obj.save()

        #c = CMSContents.objects.get(id=obj.id)
        #instance.content.add(c)
        #print(type(instance))

## register the signal
#post_save.connect(create_default_content, sender=CMSEntries, dispatch_uid="CREATE_CONTENT")

