from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    """По i берём нужный элемент из массива"""
    return indexable[i]


