from django.shortcuts import render
from django.views import View
# Create your views here.

from . pages import Page

class PageView(View):

    def get(self, request, *args, **kwargs):
        
        path = kwargs.get("path", None)
        page = Page.load(path)
        return page