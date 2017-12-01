from MarketPlace.models import Catalogo_Producto
from MarketPlace.utils import cantidad_disponible_producto_catalogo


def agregar_producto_carrito(request, product_id, quantity):
    product = Catalogo_Producto.objects.get(id=product_id)
    cantidad_disponible = cantidad_disponible_producto_catalogo(product)
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
