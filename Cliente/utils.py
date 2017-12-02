from MarketPlace.models import Catalogo_Producto
from MarketPlace.utils import cantidad_disponible_producto_catalogo, get_or_create_week, get_id_cooperativa_global


def agregar_producto_carrito(request, product_id, quantity):
    product = Catalogo_Producto.objects.get(fk_producto_id=product_id,
                                            fk_catalogo__fk_cooperativa_id=get_id_cooperativa_global(request),
                                            fk_catalogo__fk_semana=get_or_create_week())
    cantidad_disponible = cantidad_disponible_producto_catalogo(product, get_id_cooperativa_global(request))
    cart = request.session.get('cart', None)
    if not cart:
        cart = {
            'items': [{
                'product_id': product_id,
                'quantity': quantity,
                'name': product.fk_producto.nombre,
                'image': product.fk_producto.imagen.url,
                'price': float(product.precio),
                'unit': product.fk_producto.unidad_medida,
                'cantidad_disponible': cantidad_disponible
            }]
        }
    else:
        items = cart.get('items', [])
        exists = False
        i = 0
        while not exists and i < len(items):
            item = items[i]
            if item['product_id'] == product_id:
                new_quantity = item['quantity'] + quantity
                if new_quantity > cantidad_disponible:
                    new_quantity = cantidad_disponible
                item['quantity'] = new_quantity
                exists = True
            i += 1
        if not exists:
            items.append({
                'product_id': product_id,
                'quantity': quantity,
                'name': product.fk_producto.nombre,
                'image': product.fk_producto.imagen.url,
                'price': float(product.precio),
                'unit': product.fk_producto.unidad_medida,
                'cantidad_disponible': cantidad_disponible
            })
        cart['items'] = items
    return cart
