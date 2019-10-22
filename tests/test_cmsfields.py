import unittest
import mock

import os
import sys
from dataclasses import dataclass

import django

from . test_utils import initialize_django
initialize_django()

from django.core.exceptions import ObjectDoesNotExist

from mycms.models import Node
from mycms.models import PageType
from mycms.models import CMSModelTextField


from mycms.pages import BasePage
from mycms import cmsfields
from mycms.serializers import PageSerializerBase



    



class CMSTextFieldTests(unittest.TestCase):
    
    
     def setUp(self):
          #create a node to test with 
          pt = PageType.objects.get(class_name="ArticlePage")
          
          
          self.test_node, c = Node.objects.get_or_create(path="/articlepage_test",
                                                         page_type=pt,
                                                         title="ArticlePageTest")

          content = "This is a simple content."
          self.content , c = CMSModelTextField.objects.get_or_create(node=self.test_node,
                                                                     content=content,
                                                                     name="content")

     def tearDown(self):
          self.content.delete()
          self.test_node.delete()
        
          
     
     def test_instance(self):
          """
          Test instance to see if we can create and initialize
          """
          
          x = cmsfields.CMSTextField()
          x.initialize(self.test_node.pk,"content")
          
          obj = x.get_object()
          
     def test_can_get_serializer(self):
          """
          Ensure we can get back the correct serializer.
          """
          x = cmsfields.CMSTextField()
          x.initialize(self.test_node.pk, "content")
          
          serializer_class = x.get_serializer()
          
          
          
     def test_can_get_data(self):
          pass
          