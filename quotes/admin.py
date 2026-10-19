from django.contrib import admin
from .models import Quote, Author, Tag

admin.site.site_header = 'Quotes administration'
admin.site.site_title = 'Quotes admin'
admin.site.index_title = 'Manage quotes and accounts'

admin.site.register(Tag)
admin.site.register(Quote)
admin.site.register(Author)
