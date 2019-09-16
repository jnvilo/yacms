from django.core.exceptions import SuspiciousFileOperation
from django.template import Origin, TemplateDoesNotExist
from django.utils._os import safe_join

from django.template.loaders.filesystem import Loader as FileSystemLoader
from mycms.models import CMSAppRegistry
class Loader(FileSystemLoader):
    
    def get_dirs(self):
        """
        We want to be able to load templates also relative to the directory 
        of each cmsapp. This custom loader looks inside the directory 
        of each cmsapp just like the filesystemloader.
        """
    
        #self.dirs = ["/home/jnvilo/Projects/docker-websites/mycms/mycms/cmsapps/category/templates/"]
        
        #Get the directory of each cmsapp defined in the database.
        
        dirs =  CMSAppRegistry.get_cmsapp_template_dirs()
        print("returning cmsapp tempalte dirs {}".format(dirs))
        return dirs
