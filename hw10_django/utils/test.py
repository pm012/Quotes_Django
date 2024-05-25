import os
import django
from django.db.models import Count


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10_django.settings")
django.setup()

from quotes.models import Quote, Tag, Author



if __name__ =="__main__":
     top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
     for tag in top_tags:
          print(f"name: {tag.name} count: {id}")

