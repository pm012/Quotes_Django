from django import template

register = template.Library()


@register.filter
def tagslist(tags):
    return [str(name) for name in tags.all()]

@register.filter
def tags(tags):
    return ", ".join([f"#{name}" for name in tags.all()])


#register.filter('tagslist', tagslist)
#register.filter('tags', tags)