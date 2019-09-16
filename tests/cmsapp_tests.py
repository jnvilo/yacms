from mycms import wingdbstub
#Imports
import unittest
import mock

from random import randint
import loremipsum

import os
import django
import sys

##
#
# To run this tests you need to ensure you have set environment variables
# export DJANGO_SETTINGS_MODULE="website.settings"
# export PYTHONPATH="/home/jnvilo/Projects/docker-websites/theusefuldesktop.com/website"
#
##

sys.path.append("../demo_app/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")


django.setup()


#Django Imports
from django.test import TestCase
from django.template.defaultfilters import slugify
from django.http import HttpRequest
#Local Application Imports

import mycms
from mycms import exceptions
from mycms.models import CMSNode
from mycms.models import CMSAppRegistry
from django.test.client import RequestFactory

from mycms.cmsapps.category.view import PageData


class PageDataTests(unittest.TestCase):

    def test_decorator_cms_attribute(self):
        pass


    def test_categories(self):

        rf = RequestFactory()
        request = rf.get('/cms/cmsapp')

        pd = PageData(request)
        pd.categories()

        pd2 = PageData()
        pd.categories()

        for i in dir(pd):
            print(i)

class CMSNodeTests(unittest.TestCase):

    def setUp(self):
        #Ensure we have the entry in the database.
        cmsapp,_ = CMSAppRegistry.objects.get_or_create(name="category",
                                                      module="mycms.cmsapps.category",
                                                      display_name="Category")

        #create the /cmsroot category node.

        cmsnode,_ = CMSNode.objects.get_or_create(path="/cmsapp", cmsapp=cmsapp)







class TestCMSAppRegistry(unittest.TestCase):

    def setUp(self):
        """
        CMSAppRegistry test assumes we have a cmsapp called category.(This
        is the basic cmsapp.)
        """

        #Ensure we have the entry in the database.
        cmsapp,_ = CMSAppRegistry.objects.get_or_create(name="category",
                                                      module_name="mycms.cmsapps.category",
                                                      display_name="Category")

        #create the /cmsroot category node.

        cmsnode,_ = CMSNode.objects.get_or_create(path="/cmsapp", cmsapp=cmsapp)

    def test_get_cmsapp_dirs(self):
        """
        Expected outcome is a list of directories
        """
        dirs = CMSAppRegistry.get_cmsapp_dirs()
        for i in dirs:
            print(i)



    def test_get_cmsapp_template_dirs(self):

        template_dirs = CMSAppRegistry.get_cmsapp_template_dirs()

        print(template_dirs)



    def test_can_get_property_controller_class(self):

        rf = RequestFactory()
        request = rf.get('/cms/cmsapp')

        cmsnode = CMSNode.objects.get(path="/cmsapp")


    def test_get_api_urls(cls):

        CMSAppRegistry.get_api_urls()


if __name__ == '__main__':
    print("running tests")
    unittest.main()
