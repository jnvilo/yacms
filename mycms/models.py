from django.db import models
from django.contrib.auth.models import AbstractUser


class CMSUser(AbstractUser):
    pass


def __str__(self):
    return self.email


class PageType(models.Model):
    """
    Stores meta information about a page type. 
    """

    display_name = models.CharField(max_length=32, null=True)
    class_name = models.CharField(max_length=32)
    base_path = models.CharField(max_length=32, default="/cms")
    template = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.class_name


class Template(models.Model):
    name = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name


class Node(models.Model):
    """
    Node 
    """

    path = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=32, default="Not Set")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey("CMSUser", on_delete=models.DO_NOTHING, null=True)
    parent = models.ForeignKey("Node", on_delete=models.PROTECT, null=True, blank=True)
    page_type = models.ForeignKey(PageType, on_delete=models.PROTECT, null=True)
    template = models.ForeignKey(
        Template, null=True, blank=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.path

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        if self.pk is None:
            """
            This means it is just being created. We set some defaults for
            attributes that have no entries. 
            """

            if self.owner is None:
                # The guest user is guaranteed to exist because it is created
                # in the apps.py.
                self.owner = CMSUser.objects.get(username="guest")

            if self.page_type is None:
                # The Page class is guaranteed to exist.
                self.page_type = PageType.objects.get(class_name="Page")

        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )


class CMSModelField(models.Model):

    """A lame attempt at obsfucating the name of these model fields
    such that any child classes will hopefully decide not clash with 
    the following two fields.
    """

    cmsmodelfield_node_9824 = models.ForeignKey("Node", on_delete=models.PROTECT)
    cmsmodelfield_name_9824 = models.CharField(max_length=92, null=False)


class CMSModelTextField(CMSModelField):

    content = models.TextField(max_length=4096, null=True, default="No Content")

    def __str__(self):
        return self.content


class CMSContentModelField(CMSModelField):

    content = models.TextField(max_length=4096, null=True, default="No Content")
