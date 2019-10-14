import sys
import os
import django

def initialize_django():
    
    sys.path.append("../mycms_demo/")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    django.setup()

