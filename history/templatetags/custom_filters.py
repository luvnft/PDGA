from django import template
import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def current_year():
    return datetime.datetime.now().year
