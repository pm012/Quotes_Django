from django.contrib import admin
from .models import Quote, Author, Tag

# Register your models here.
admin.site.register(Tag)
admin.site.register(Quote)
admin.site.register(Author)
