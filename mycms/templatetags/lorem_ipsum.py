from django import template
from django.utils import lorem_ipsum
from django.utils.safestring import mark_safe

from random import randint

register = template.Library()


@register.simple_tag
def lorem_paragraphs(num_paragraphs=None):

    if num_paragraphs == None:
        num_paragraphs = randint(5, 10)

    results = []
    paragraphs = lorem_ipsum.paragraphs(num_paragraphs, common=False)

    for paragraph in paragraphs:
        results.append("<p>{}</p>".format(paragraph))

    return mark_safe("\n".join(results))
