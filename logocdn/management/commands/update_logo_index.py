from django.core.management.base import BaseCommand, CommandError


from pathlib import Path
from logocdn.models import LogoEntries
from logocdn.models import LogoTags
from logocdn.models import logo_types
from django.conf import settings
from django.db.models import Q

from logocdn import wingdbstub

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        
        
        
        #self.create_entries(settings, logo_types, LogoTags, LogoEntries)

        #LogoEntries.objects.all().delete()
        self.create_entries()

    def create_entries(self):
      
        for file in Path(settings.SVG_LOGOS_PATH).iterdir():
            file_type = file.name[file.name.rfind(".")+1:].upper()
            
            if file_type in logo_types():                
                print("Processing {}".format(file.name))
                logo_entry, c= LogoEntries.objects.get_or_create(file_name=file.name)
                
                
                                                           