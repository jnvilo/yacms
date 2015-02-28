from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from creole import creole2html
from random import randrange
import loremipsum
import arrow

from bs4 import BeautifulSoup
from django.http import JsonResponse

from django.core.cache import cache


from .base import BaseView
from .base import register
from .creole_macros import code
from .creole_macros import pre
from .creole_macros import html



