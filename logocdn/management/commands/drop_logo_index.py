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
        
        
        LogoEntries.objects.all().delete()
                                                           