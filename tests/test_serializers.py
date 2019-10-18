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
from mycms.pages import BasePage
from mycms import cmsfields
from mycms.serializers import PageSerializerBase
class TestBasePage(BasePage):
    
     node = cmsfields.CMSNodeField()

class BasePageSerializerTests(unittest.TestCase):
    
     def setUp(self):
          #create a node to test with 
          
          self.test_node, c = Node.objects.get_or_create(path="/basepageserializertests")
          
     
     def tearDown(self):
          
          if hasattr(self, "test_node"):
               self.test_node.delete()
    
     def test_can_build_serializer(self):
    
          data = { "node": self.test_node}
          
          SerializerClass = TestBasePage.build_serializer()

          serializer = SerializerClass(instance=data)
          print(serializer.data)
          
          data = { "node": self.test_node}
          
          s = PageSerializerBase(instance=data)
          print(s.data)