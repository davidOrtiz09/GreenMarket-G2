from django import template
from MarketPlace.utils import cantidad_disponible_producto_catalogo

register = template.Library()


@register.filter(name='get_cantidad_disponible_producto_catalogo')
def get_cantidad_disponible_producto_catalogo(producto_catalogo):
    return cantidad_disponible_producto_catalogo(producto_catalogo)
