from django import template
register = template.Library()


@register.inclusion_tag('mycms/templatetags/file_upload.html')
def file_upload():
    #Nothing to add to the context for now.
    return { "none": None }
