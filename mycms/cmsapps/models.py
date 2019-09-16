"""
Contains CMSApps models. 

"""
import os
import functools
import inspect
from rest_framework import viewsets #added for use in CMSAppRegistry
from rest_framework import routers  #added for use in CMSAppRegistry
from mycms.funclib import raw #added for use in CMSAppRegistry

from django.db import models

__all__ = ['CMSAppRegistry','CMSNode']

class CMSAppRegistry(models.Model):
    """
    A database table that stores the information about the different cmsapps.
    It also provides helper methods to easily get data from the registered
    cmsapps. 
    
    """
    
    name = models.CharField(max_length=128, unique=True, null=True,help_text="Identifier for the cmsapp. By convention its the module name.")
    module_name = models.CharField(max_length=128, null=True,help_text="The module name for the cmsapp.")
    display_name = models.CharField(max_length=128,null=True, help_text="Pretty name to display in lists and admin interfaces.")    
    
    def save(self, *args, **kwargs):
        if self.display_name is None:
            self.display_name == self.name
        return super(CMSAppRegistry, self).save(*args,**kwargs)
    
    @classmethod
    @functools.lru_cache(maxsize=100000000)
    def get_cmsapp_dirs(cls):
        """
        Returns a list of directories where the cmsapps reside. It gets
        the list of cmsapp module names and instantiates them so that 
        we can find the path where they reside and returns that as a list
        of directories
        """
        apps = cls.as_list()
    
        cmsapp_dirs = []
        for app in apps:
            
            module_name = app.module_name
        
            parts = module_name.split(".")[1:]
            module = __import__(module_name)
            for part in parts:
                module = getattr(module, part)
            path = os.path.dirname(module.__file__)
            cmsapp_dirs.append(path)


        return(cmsapp_dirs)
    
    @classmethod
    def register_serializers(cls):
        """
        Load all serializers for each of the cmsapps. 
        """
        
        cmsapps = CMSAppRegistry.as_list()
        
        for cmsapp in cmsapps:
            #load the serializer module.
            modoule_name = "{}.serializers"
            serializer_module = import_module(module_name)
        
        
    @classmethod 
    def get_cmsapp_subdir(cls, dirname):
        cmsapp_dirs = cls.get_cmsapp_dirs()
        cmsapp_template_dirs = []
        
        for cmsapp_dir in cmsapp_dirs:
            #cmsapp_template_dirs.append(Path(cmsapp_dir, dirname).as_posix())
            pass
        return cmsapp_template_dirs        
    
    @classmethod 
    def get_cmsapp_static_dirs(cls):
        return cls.get_cmsapp_subdir("static")
    
    @classmethod
    @functools.lru_cache(maxsize=100000000, typed=False)   
    def get_cmsapp_template_dirs(cls):
        """
        Returns a list of all template dirs for each cmsapp module.
        """
        return cls.get_cmsapp_subdir("templates")
            
    @classmethod
    @functools.lru_cache(maxsize=100000000, typed=False)    
    def as_list(cls):
        """
        Returns the cmsapp entries from the database.
        """
        apps = CMSAppRegistry.objects.all()
        return apps
    
    
    @classmethod 
    @functools.lru_cache(maxsize=100000000, typed=False)   
    def import_module(cls,module_name):
        """
        A method to import a module name. This is just a copy of the global 
        function of the same name. 
        """
        parts = module_name.split(".")[1:]
        module = __import__(module_name)
        for part in parts:
            module = getattr(module, part)
        
        return module    
 
    @property
    def cmsapp_module(self):
        """This imports the module for the cmsapp."""
        
        module = import_module(self.cmsapp.module_name)
        return module
    
    @property
    def pageview_class(self):
        """
        Returns the pageview class of the cmsapp.
        """
       
        pageview_module = import_module(self.module_name + ".view")
        pageview_cls = getattr(pageview_module,"PageView")
        return pageview_cls
    
        
    def __str__(self):
        return self.name
    
    @classmethod
    @functools.lru_cache(maxsize=100000000, typed=False)  
    def get_api_urls(cls):
        
        router = routers.DefaultRouter()
        
        for app in CMSAppRegistry.as_list():
            #load the module for each app api.py
            try:
                module_name = app.module_name + ".api"
                api_module = import_module(module_name)
                
                for name, obj in inspect.getmembers(api_module):
                    if inspect.isclass(obj):
                        if (issubclass(obj, viewsets.ModelViewSet) or 
                           issubclass(obj, viewsets.ViewSet)):
                            cls.__add_router_entry(obj, name, router)

            except ModuleNotFoundError as e:
                print("Failed to find module: {}".format(module_name))
                pass
        return router.urls
    @classmethod
    def __add_router_entry(cls, obj, name, router):
         
        api_base_name = getattr(obj, "api_base_name",None)
        api_path = getattr(obj,"api_path", None)
        
        if api_base_name is None:
            api_base_name = name.lower()
            
        if api_path is None:
            api_path = raw("api/v2/{}".format(name.lower())) 
        
        print("adding router url: {},{},base_name={}".format(api_path,name,api_base_name))
        router.register(api_path, obj, base_name=api_base_name)   
          
        return router.urls
         
    
@functools.lru_cache(maxsize=100000000, typed=False)      
def import_module(module_name):

    parts = module_name.split(".")[1:]
    module = __import__(module_name)
    for part in parts:
        module = getattr(module, part) 
    return module
       
class CMSNode(models.Model):
    """
    The CMSNode is a database table stores that attributes about any node within mycms.
    Every entry within MYCMS is a node. (Just like inodes in a filesystem.) 
     
    cmsapp = CMSAppRegistry.objects.get(name="category")
    cmsnode = CMSNode.objects.get_or_create(path="/cmsapp", cmsapp=cmsapp)
    """
    
    path = models.CharField(max_length=2000, unique=True,help_text="Path to the node. example: /cms/category/file")    
    parent = models.ForeignKey("CMSNode", null=True, blank=True, help_text=" A foreinkey to the parent path.",
                               on_delete=models.DO_NOTHING, related_name="parentpath")    
    cmsapp = models.ForeignKey(CMSAppRegistry, on_delete=models.DO_NOTHING, help_text="Foreignkey to the cmsapp")
    
    
    def __str__(self):
        return self.path
        
    def get_cmsapp(self, request,  **kwargs):
        """ 
    
        Returns an instance of a CMSPage.
        
        For example:
        
        cmspages/login
        cmspages/logout
        cmspages/singlepage
        cmspages/pagelist.
        """
    
        PageView = self.cmsapp.pageview_class
        pageview =  PageView(request, self)
        pageview = pageview.pageview
        return pageview
    
    def get_pageview(self,request):
        """
        Returns the pageview for the cmsapp. 
        """
        
        PageView = self.cmsapp.pageview_class
        return PageView(request, self)      
    
    def page(self):
        """
        returns html of the page.
        """ 
        pass
    
        
 
    
