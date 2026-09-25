from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100, unique=True)
    born_date = models.CharField(max_length=50, blank=True)
    born_location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fullname']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self) -> str:
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return self.name


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='quotes')
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='quotes',
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote'
        verbose_name_plural = 'Quotes'

    def __str__(self) -> str:
        return f'"{self.quote[:50]}..." - {self.author.fullname if self.author else "Unknown"}'