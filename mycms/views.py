from django.shortcuts import render
from django.views import View

# Create your views here.

from .pages import Page


class IndexPage(View):
    def get(self, request, *args, **kwargs):

        return render(request, "mycms/Index.html")

class SandboxView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "mycms/sandbox.html")
    

class PageView(View):
    def get(self, request, *args, **kwargs):

        path = kwargs.get("path", None)

        """
        Page.load() will create the correct page subclass instance according
        to the given path. This , the actual instance created is a
        subclass of Page or it can even be an HttpResponse instance.
        """

        page = Page.load(path, request)

        """
        The page instance has a response method so we can just return it 
        because  django will detect the presence of the response method
        and will call it. We could also do return page.response().
        """
        return page


    