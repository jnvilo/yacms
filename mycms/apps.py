from django.apps import AppConfig
from mycms import VERSION_STRING
from django.db.utils import OperationalError
class MyCMSConfig(AppConfig):
    name = 'mycms'

    def ready(self):
        print("Loaded MyCMS Version: {}".format(VERSION_STRING))
        #pass # startup code here    
        from mycms import utils
        username="admin"
        password="password"
        email="demo@mycmsproject.org"
        
        try:
            utils.ensure_user_is_created("admin", 
                                         "admin@mycmsproject.org", 
                                         "password",
                                         superuser=True)
            
            utils.ensure_user_is_created("guest", 
                                         "guest@mycmsproject.oprg", 
                                         "password", 
                                         superuser=False)
      
            from mycms.pages import Page
            from mycms.pages import PageRegistry
            from mycms.models import Node
            
            PageRegistry.sync_pagetypes_to_db()
            
            #Make sure "/" exists
            index_node, c = Node.objects.get_or_create(path="/")
                        
                  
        except OperationalError as e:
            """
            The database is not yet created.
            """
            pass
        
        except Exception as e:
            print(e)
            import sys
            sys.exit()
            
        
      
        
        