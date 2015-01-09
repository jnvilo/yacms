from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from django.shortcuts import render_to_response, redirect

from django.db.models import Q

from . base import BaseView
from . base import register
from  yacms.models import Pages

class CategoryView(BaseView):

    def get_child_categories(self):

        path_obj = self.page_obj.path
        children = Pages.objects.filter(path__parent=path_obj, page_type="CATEGORYVIEW").order_by("path")       
        return children


    def iter_child_categories(self):

        path_obj = self.page_obj.path
        children = Pages.objects.filter(path__parent=path_obj, page_type="CATEGORYVIEW")

        for each in children:
            yield each.view

    def iter_child_html_pages(self):

        path_obj = self.page_obj.path
        q_filter = Q(page_type="HTMLVIEW") | Q(page_type="MULTIPAGEINDEX")
        children = Pages.objects.filter(path__parent=path_obj).filter(q_filter).order_by("-date_created")
        
        for each in children:
            yield each.view


register("CATEGORYVIEW", CategoryView, "Category")