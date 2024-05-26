
from django import template
from ..models import Author

register = template.Library()

@register.filter
def author(id_):
    author = Author.objects.get(pk=id_)
    return author.fullname
