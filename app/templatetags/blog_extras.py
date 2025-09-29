from django import template
from ..models import Category, Tag

register = template.Library()

@register.simple_tag
def get_categories():
    return Category.objects.all()

@register.simple_tag
def get_tags():
    return Tag.objects.all()

@register.filter
def truncate_words(value, arg):
    try:
        words = value.split()
        if len(words) > arg:
            return ' '.join(words[:arg]) + '...'
        return value
    except:
        return value