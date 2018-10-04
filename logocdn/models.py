from django.db import models
from pathlib import Path
from django.db.models.signals import post_save


LOGO_FILETYPE_CHOICES = (
    ("SVG", "svg"),
    ("PNG", "png"),
    ("BMP", "bmp"),
    ("JPG", "jpg"),
)


def logo_types():
    """A generator to get all the logo types that we support"""
    for logo_type_tuple_entry  in LOGO_FILETYPE_CHOICES:
        logo_type , _ = logo_type_tuple_entry
        yield(logo_type)
    

class LogoTags(models.Model):
    tag = models.CharField(max_length=32)

    def __str__(self):
        return self.tag
    
class LogoEntries(models.Model):
    
    file_name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=1024, null=True, blank=True)
    display_title = models.CharField(max_length=256,null=True, blank=True)
    file_type = models.CharField(max_length=16, choices=LOGO_FILETYPE_CHOICES, null=True, blank=True)
    tags = models.ManyToManyField(LogoTags, null=True, blank=True)
    
    def __str__(self):
        return self.short_name
    
    def save(self,*args, **kwargs):
        
        
        if self.short_name is None:
            self.short_name  = self.file_name[:self.file_name.rfind(".")]  
            
            if self.display_title is None:
                self.display_title = self.short_name
         
        if self.file_type is None:
            self.file_type = self.file_name[self.file_name.rfind(".")+1:].upper()
        super().save(*args, **kwargs)            
    
    @classmethod
    def post_save(cls, sender, instance, created, *args, **kwargs):
    
        tag, c = LogoTags.objects.get_or_create(tag=instance.short_name)
        if c:
            #tag was just created. we can just add to instance
            instance.tags.add(tag)
        elif instance not in tag.logoentries_set.all():
            
            #not newly created, we need to check first if we already ahve tag
            instance.tags.add(tag)
            
            
            
post_save.connect(LogoEntries.post_save, sender=LogoEntries)