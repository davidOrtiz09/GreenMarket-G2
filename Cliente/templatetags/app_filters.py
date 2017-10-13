from django import template

register = template.Library()


@register.filter(name='get_error')
def get_error(dictionary, key):
    return dictionary.get(key)
