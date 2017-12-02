from django import template

register = template.Library()


@register.filter(name='get_error')
def get_error(dictionary, key):
    return dictionary.get(key)

@register.filter(name='get_len')
def get_len(list):
    return len(list)

@register.filter(name='is_favorito')
def is_favorito(producto,cliente):
    return not(cliente is None) and producto.fk_producto.favorito_set.filter(fk_cliente=cliente).count() > 0
