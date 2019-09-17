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
from mycms.cmsapps.skeleton import CMSAppSkeleton

class PageDataTests(unittest.TestCase):

    def test_init(self):
        csa = CMSAppSkeleton("index")
        

    def test_create_cmsapp(self):
        csa = CMSAppSkeleton("index")
        csa.create_cmsapp()

  


