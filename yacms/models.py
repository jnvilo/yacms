from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import pathlib
from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify





class Paths(models.Model):
    path = models.CharField(max_length=1024, default="/")
    parent = models.ForeignKey("Paths", null=True)

    def save(self, *args, **kwargs):    

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
        return PageViewClass(self)

    def save(self, *args, **kwargs):    

        if self.slug is None:
            self.slug = slugify(self.title)

        if self.template is None:
            self.template = "{}.html".format(self.page_type.lower()) 
        super(Pages, self).save(*args, **kwargs)


    def response(self,request, **kwargs):    
        return self.view.response(request, **kwargs)



    def get_absolute_url(self):

        path = self.path.path

        if not path.startswith("/"):
            path = "/{}".format(path)
        return "/cms{}".format(path)

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

        path = self.path.path
        title = self.title

        key_name = "{0}:{1}:{2}".format("introduction",path, title)  

        from django.core.cache import cache
        value = cache.get(key_name)

        if not value:

            from creole import creole2html
            from bs4 import BeautifulSoup
            html = creole2html(self.content)

            soup = BeautifulSoup(html)

            p = soup.find("p")

            value = str(p)
            value = value.lstrip("<p>")
            value = value.rstrip("</p>")

            cache.set(key_name, value)

        return value
