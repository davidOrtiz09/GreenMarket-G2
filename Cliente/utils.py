from MarketPlace.models import Catalogo_Producto


def agregar_producto_carrito(request, product_id, quantity):
    product = Catalogo_Producto.objects.get(id=product_id)
    cart = request.session.get('cart', None)
    if not cart:
        cart = {
            'items': [{
                'product_id': product_id,
                'quantity': quantity,
                'name': product.fk_producto.nombre,
                'image': product.fk_producto.imagen.url,
                'price': float(product.precio),
                'unit': product.fk_producto.unidad_medida
            }]
        }
    else:
        items = cart.get('items', [])
        exists = False
        i = 0
        while not exists and i < len(items):
            item = items[i]
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                exists = True
            i += 1
        if not exists:
            items.append({
                'product_id': product_id,
                'quantity': quantity,
                'name': product.fk_producto.nombre,
                'image': product.fk_producto.imagen.url,
                'price': float(product.precio),
                'unit': product.fk_producto.unidad_medida
            })
        cart['items'] = items
    return cart
