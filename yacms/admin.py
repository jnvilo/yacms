from django.contrib import admin
from yacms.models import Paths
from yacms.models import Pages


class PathsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Paths, PathsAdmin)

class PagesAdmin(admin.ModelAdmin):
    list_filter = ('path__parent', 'date_created', "published", "frontpage", "page_number")

admin.site.register(Pages, PagesAdmin)


    
