from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

#Imports
from random import randint
import loremipsum

#Django Imports
from django.test import TestCase
from django.template.defaultfilters import slugify
from django.http import HttpRequest
#Local Application Imports
from yacms import exceptions
from yacms import pageview
from yacms.models import Pages
from yacms.models import Paths

class PagesModelTests(TestCase):
    
    
    def test_create_page(self):
        
        amount = randint(5, 15)
        content = loremipsum.generate_paragraphs(amount)
        title = "This is my page title"
        
        path , created = Paths.objects.get_or_create(path="/foo/bar/baz/{}".format(slugify(title)))
        
        page = Pages()
        page.content = content
        page.title = title
        page.path=path
        page.page_type = "HTML"
        page.save()
        
        self.assertEqual(page.content, content)
        self.assertEqual(page.title, title)
        self.assertEqual(page.page_type, "HTML")
        self.assertEqual(page.slug, slugify(title))
        self.assertEqual(page.path.path,"/foo/bar/baz/{}".format(slugify(title)))
        
    def test_PageView_view(self):
           
        #Create a Page entry to use for our test.
        amount = randint(5, 15)
        content = loremipsum.generate_paragraphs(amount)
        title = "This is my page title"
        path , created = Paths.objects.get_or_create(path="/foo/bar/baz/{}".format(slugify(title)))
        
           
        page, created = Pages.objects.get_or_create( content = content,
                                               title = title,
                                               page_type = "HTML",
                                               path=path,
                                               )
        #Create a fake request and kwargs
        request = HttpRequest()
        request.path = "/cms/foor/bar/baz"
        kwargs = {}
        
        page.set_args(request, **kwargs)        
        view = page.view
        self.assertTrue(isinstance(view, pageview.PageView))
        



class PageViewTests(TestCase):
    
    def test_fn_register(self):

        class BadPageView():
            pass
        
        page_type = "HTML"
        page_class = BadPageView

        with self.assertRaises(exceptions.IncompatiblePageClass):
            
            pageview.register(page_type, page_class)
        
    def test_fn_get_page_class(self):
        
        page_type = "HTML"
        page_class = pageview.PageView
        
        pageview.register(page_type, page_class)
        result_class = pageview.get_page_class(page_type)
        
        self.assertEqual(result_class, page_class)
        
        
   
class BaseViewTests(TestCase):
    
    def setUp(self):
        #create a test page
        amount = randint(5, 15)
        content = loremipsum.generate_paragraphs(amount)
        title = "This is my page title"
        
        path , created = Paths.objects.get_or_create(path="/foo/bar/baz/{}".format(slugify(title)))
        
        page = Pages()
        page.content = content
        page.title = title
        page.path=path
        page.page_type = "BASE"
        page.save()
        
        self.page = page
        
    def test_instantiace_BaseView(self):
        from yacms.pageview.base import BaseView
        from yacms.pageview.base import register
        from django.http import HttpRequest
        
        
        register("BASE", BaseView)

        #Create a fake request and kwargs
        request = HttpRequest()
        request.path = "/cms/foor/bar/baz"
        kwargs = {}
        
        self.page.set_args(request, **kwargs)
        view = self.page.view
        
        
        #the view should give us a template.
        self.assertEqual(view.page_obj.template, "base.html")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
    
    
    
    
        

    
    
    