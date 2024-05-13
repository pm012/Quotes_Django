from django.db import models
#from mongoengine import  Document, StringField, ListField, ReferenceField

# Define MongoDB models
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False, unique=True)


class Quote(models.Model):
    id = models.AutoField(primary_key=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

