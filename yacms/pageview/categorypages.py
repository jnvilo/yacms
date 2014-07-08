from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from django.shortcuts import render_to_response, redirect

from . base import BaseView
from . base import register


class CategoryView(BaseView):
    pass
    

register("CATEGORYVIEW", CategoryView)