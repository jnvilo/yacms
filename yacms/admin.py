from django.contrib import admin
from .models import CMSPageTypes
from .models import CMSContents
from .models import CMSEntries
from .models import CMSMarkUps
from .models import CMSTemplates
from .models import CMSPaths

@admin.register(CMSPaths)
class CMSPathsAdmin(admin.ModelAdmin):
    pass

@admin.register(CMSContents)
class CMSContents(admin.ModelAdmin):
    pass

@admin.register(CMSEntries)
class CMSEntries(admin.ModelAdmin):
    pass

@admin.register(CMSMarkUps)
class CMSMarkUps(admin.ModelAdmin):
    pass

@admin.register(CMSTemplates)
class CMSTemplates(admin.ModelAdmin):
    pass

@admin.register(CMSPageTypes)
class CMSPageTypesAdmin(admin.ModelAdmin):
    list_filter = ("page_type", "text", "view_class")
    


    
