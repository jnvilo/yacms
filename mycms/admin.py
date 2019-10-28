# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CMSUserCreationForm, CMSUserChangeForm
from .models import CMSUser
from .models import PageType
from .models import Node
from .models import CMSModelField
from .models import CMSContentModelField
from .models import CMSModelTextField
from .models import Template


@admin.register(CMSUser)
class CMSUserAdmin(UserAdmin):
    add_form = CMSUserCreationForm
    form = CMSUserChangeForm
    model = CMSUser
    list_display = ["email", "username"]


@admin.register(PageType)
class PageTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "display_name", "class_name", "base_path"]


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ["id", "path", "title", "created", "modified"]


@admin.register(CMSModelField)
class CMSModelFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(CMSContentModelField)
class CMSContentModelField(admin.ModelAdmin):
    pass


@admin.register(CMSModelTextField)
class CMSModelTextField(admin.ModelAdmin):
    pass


@admin.register(Template)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
