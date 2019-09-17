import sys
from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist
from django.shortcuts import render
from django.template import Context

class CMSPageData(Context):


    page_attributes = ["get_absolute_url", "title","ancestors"]
    
    

    def __init__(self, request, node, dict_=None, autoescape=True, use_l10n=None, use_tz=None):
        self.request = request
        self.node = node
        super().__init__(dict_=dict_, autoescape=autoescape, use_l10n=use_l10n, use_tz=use_tz)


    def title(self):
        """
        The title is taken from the cmsnode
        """
        return self.node.title

    def ancestors(self):
        """
        Returns a list of the ancestor nodes. Ancestor Nodes
        are the parent nodes and grandparents all the way to the root node.
        It is returned as a list.
        """

        node_list = []
        node = self.node
        while node != None:
            node_list.append(node)
            node = node.parent

        node_list.reverse()
        return node_list   

    def add_to_context(self,attribute):
        pass

    def get_absolute_url(self):
        self.node.cmsapp.get_absolute_url()

    def flatten(self):
        #override flatten so that we have a chance to add the other
        #methods
        unwanted_attributes = dir(CMSPageData)
        all_attributes = dir(self.__class__)


        attribute_dicts = {}
        for attribute in all_attributes:
            if ((attribute not in unwanted_attributes) or (attribute in self.page_attributes)):
                attribute_dicts.update({attribute:getattr(self,attribute)})
            self.dicts.append(attribute_dicts)
        return super().flatten()




class CMSPageView:
    """
    Base class for all CMSApp views.
    """

    def __init__(self, node):
        self.node = node


    @property
    def request(self):
        return self._request


    @request.setter
    def request(self, value):

        self._request = value



    def user(self):
        """
        Returns the current user. None if not logged in.
        """
        pass



    def render(self):
        """
        The render function returns the rendered HTML page. The instance of this
        controller app is returned as a response object and Django calls this
        render function to get the HTML page.

        Logic to produce all the atributes for the template can be done here.
        """
        self.template = self.Meta.TEMPLATE

        pagedata = self.Meta.PAGEDATA(self.request, self.node)
        pagedata["foo"] = "Hello"
        pagedata["bar"] = "world"

        if self.template == None:
            raise Exception("No TEMPLATE parameter provided inside the Controller.")
        return render(self.request, self.template, pagedata.flatten())




from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from mycms.cmsapps.models import CMSNode



class CMSAppModeViewSset(viewsets.ModelViewSet):

    pass

