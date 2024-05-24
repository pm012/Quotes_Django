
from django import template
from ..models import Author

from hw10_django.utils import conect

register = template.Library()

def get_author(id_):
    #db = conect.get_mongo_connection()
    author = Author.objects.get(pk=id_)
    return author.fullname

register.filter('author', get_author)