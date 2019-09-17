import os
from pathlib import Path

class CMSAppSkeleton:

    def __init__(self, name):
        self.name = name
        whereiam = os.path.abspath(__file__)
        
        skeleton_dir,_ = os.path.split(whereiam)
        self.cmsapps_dir,_ = os.path.split(skeleton_dir)
        print(self.cmsapps_dir)
        
    def create_cmsapp(self):    
        cmsapp_path = Path(self.cmsapps_dir, self.name)
        templates_path = Path(cmsapp_path,"templates",self.name)
        static_path = Path(cmsapp_path,"static",self.name)
    
        try: 
            cmsapp_path.mkdir(parents=True)
        except FileExistsError as e: 
            pass
        
        try:
            templates_path.mkdir(parents=True)
        except FileExistsError as e:
            pass
        
        try:
            static_path.mkdir(parents=True)
        except FileExistsError as e:
            pass
        
    def create_files(self):
        #create files [name/views.py,name, 
        #templates/name.html, 
        #name/{api.py, 
        #serializers.py, 
        #view.py, 
        #__init__.py}
        pass
    
    def create_view_file(self):
        pass
    
    def create_api_file(self):
        pass
    
    def create_serializers_file(self):
        pass
    


