import unittest
import mock

import os
import sys
from dataclasses import dataclass

import django

from test_utils import initialize_django
initialize_django()

from django.core.exceptions import ObjectDoesNotExist

from mycms.models import Node
from mycms.models import PageClass

@dataclass
class NodeData:
    
    title: str
    slug : str
    path : str
    parent: int
    page_class: int

class NodeTest(unittest.TestCase):
    

    def setUp(self):
        
        #ensure we have our test root node
        self.test_root, c = Node.objects.get_or_create(path="/testroot", 
                                               parent=None)
        
    def test_save(self):
        """
        Node.save() should set default_page to "DefaultPage"
        and the slug be equal to slugify(title)
        """
        try:
            testpage = Node.objects.get(path="/testroot/testpage")
            testpage.delete()
        except Node.DoesNotExist as e:
            pass
        
        testpage = Node(path="/testroot/testpage",
                        title="This is a test")
        
        testpage.save()
        
        default_page_class = PageClass.objects.get(class_name="DefaultPage")
        self.assertEqual(testpage.page_class, default_page_class)
        self.assertEqual(testpage.title, "This is a test")
    
    def test_get_str(self):
        """
        The __str__ result should be the title. 
        """
        title = "The string is the Title"
        path = "/testroot/testpage2"
        try:
            testpage = Node.objects.get(path=path)
            testpage.delete()
        except Node.DoesNotExist as e:
            pass
        
        testpage = Node(path=path,title=title)
        testpage.save()        
        
        first = path
        second = str(testpage)
        self.assertEqual(first, second)
        
    def test_get_absolute_url(self):
        """
        This test assumes that the page_class base_url is set to /cms. This is 
        the default. 
        """
        
        url = self.test_root.get_absolute_url()
        path = "/cms/testroot"
        self.assertEqual(url, path)
    
        
    def test_save_with_no_page_class(self):
        
        try:
            node = Node.objects.get(path="/test_with_no_page_class", 
                                          title="TESt_with_no_page_class")
            node.delete()
        except ObjectDoesNotExist as e:    
            pass
        
        node = Node(path="/test_with_no_page_class", 
                    title="TESt_with_no_page_class")        
        node.save()
        
class PageClassTest(unittest.TestCase):
    
    def test_fields(self):
        
        class_name = "TestClassName"
        
        try:
            cls = PageClass.objects.get(class_name=class_name)
            cls.delete()
        except  Exception as e:
            pass
        
        cls = PageClass(class_name=class_name)
        
        self.assertEqual(cls.base_url,"/cms")
        self.assertEqual(cls.class_name, "TestClassName")
        self.assertEqual(str(cls), class_name)
        