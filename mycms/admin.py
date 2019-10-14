
# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CMSUserCreationForm, CMSUserChangeForm
from .models import CMSUser
from .models import PageType
from .models import Node

@admin.register(CMSUser)
class CMSUserAdmin(UserAdmin):
    add_form = CMSUserCreationForm
    form = CMSUserChangeForm
    model = CMSUser
    list_display = ['email', 'username',]

@admin.register(PageType)
class PageTypeAdmin(admin.ModelAdmin):
    list_display = ["id","display_name","class_name","base_path"]
    
@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ["id","path","title","created","modified"]