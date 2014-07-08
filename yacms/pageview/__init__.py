from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from  yacms.exceptions import PageClassNotFound
from  yacms.exceptions import IncompatiblePageClass

from . base import BaseView

from . categorypages import CategoryView
from . adminpages import AdminView
from . htmlpages import PageView
from . base import register
from . base import get_page_class


register("HTML", PageView)
register("CATEGORY", CategoryView)