from django import template
from MarketPlace.utils import cantidad_disponible_producto_catalogo, get_id_cooperativa_global

register = template.Library()


@register.filter(name='get_cantidad_disponible_producto_catalogo')
def get_cantidad_disponible_producto_catalogo(producto_catalogo, request):
    return cantidad_disponible_producto_catalogo(producto_catalogo, get_id_cooperativa_global(request))
