
from bson.objectid import ObjectId
from django import template

# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hw10_django.utils import conect

register = template.Library()



def get_author(id_):
    db = conect.get_mongo_connection()
    author = db.author.find_one({'_id': ObjectId(id_)})
    return author['fullname']

register.filter('author', get_author)