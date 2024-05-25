# custom_filters.py
from django import template

register = template.Library()

@register.filter
def add(value, arg):
    return value + arg * 3
