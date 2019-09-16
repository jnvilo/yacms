import sys

from django.core.management.base import BaseCommand, CommandError
from mycms.models import CMSEntries


from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from mycms.view_handlers.page_types import singlepageview_pagetype_obj
from mycms.view_handlers.page_types import multipageview_pagetype_obj
from mycms.view_handlers.page_types import allarticles_pagetype_obj
from mycms.models import CMSPath
from mycms import wingdbstub

class Command(BaseCommand):
    
    
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        
        #dynamically load a module.
        
        import sys
        import inspect
        import pkgutil
        from pathlib import Path
        from importlib import import_module  
        
        
        module_name = "mycms.management.commands.mycommand"
        parts = module_name.split(".")[1:]
        module = __import__(module_name)
        for part in parts:
            module = getattr(module, part)
    
        #at this point module will be the mycommand module as 
        #if you have done 
        #from mycms.management.commands import mycommand
    
    def make_paths(self):
        from mycms.models import CMSPath

        parent_path,_ = CMSPath.objects.get_or_create(path="/", parent=None,cmsapp="category")
        sub_1,_ = CMSPath.objects.get_or_create(path="/sub1", parent=parent_path,cmsapp="category")
        sub_2,_ = CMSPath.objects.get_or_create(path="/sub2", parent=parent_path,cmsapp="category")
        sub_3,_ = CMSPath.objects.get_or_create(path="/sub3", parent=parent_path,cmsapp="category")
        sub_sub_3 = CMSPath.objects.get_or_create(path="/sub3", parent=sub_3,cmsapp="category")


       
    def getmembers(self):
        from django.db.models import Q
        
        c = CMSEntries.objects.get(path__path="/sysadmin/linux")
        
        print(c)
        obj_list = CMSEntries.objects.filter((Q(page_type = singlepageview_pagetype_obj) | 
                                              Q(page_type = multipageview_pagetype_obj)) &
                                             Q(path__path__startswith =  c.path.path))        
        
        
        
        for obj in obj_list:
            print(obj.path)
    
    
DJANGOPROJECT = "website"
if __name__ == "__main__":
    
    from mycms.website import settings
    from django.core.management import setup_environ
    setup_environ(settings)    
    
    from django.core.management import call_command
    
    #call_command('my_command', 'foo', bar='baz')    
   
    
    call_command('sandbox')    