from django import template

register = template.Library()


@register.filter(name='get_error')
def get_error(dictionary, key):
    return dictionary.get(key)

@register.filter(name='get_len')
def get_len(list):
    return len(list)