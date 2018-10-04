from django.contrib import admin

# Register your models here.
from .models import LogoEntries
from .models import LogoTags

@admin.register(LogoEntries)
class LogoEntriesAdmin(admin.ModelAdmin):
    list_display = ['short_name',"file_name", "display_title", "file_type"]
    list_filter = ["file_type"]

@admin.register(LogoTags)
class LogoTags(admin.ModelAdmin):
    list_display = ['tag']
    