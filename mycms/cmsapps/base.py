import sys
from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist
from django.shortcuts import render
from django.template import Context

class CMSPageData(Context):
    

    
    def __init__(self):
        pass
        
    def add_to_context(self,attribute):
        pass
    

    
    
  

    
class CMSPageView:
    """
    Base class for all CMSApp views. 
    """

    
    def __init__(self, request,template):
        self.request = request
        self.template = template
        
       
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
       
        pagedata = self.Meta.PAGEDATA(self.request).flatten()
        pagedata["foo"] = "Hello"
        pagedata["bar"] = "world"
        
        if self.template == None:
            raise Exception("No TEMPLATE parameter provided inside the Controller.")
        return render(self.request, self.template, pagedata)
     



from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from mycms.cmsapps.models import CMSNode



class CMSAppModeViewSset(viewsets.ModelViewSet):
    
    pass

