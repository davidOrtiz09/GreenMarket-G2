from MarketPlace.models import Catalogo_Producto
from MarketPlace.utils import cantidad_disponible_producto_catalogo


def get_or_create_cart(request):
    cart = request.sesion.get('cart', None)
    if not cart:
        cart = {
            'items': [],
            'canastas': []
        }
    else:
        items = cart.get('items', [])
        canastas = cart.get('canastas', [])

        if not items:
            cart['items'] = []
        if not canastas:
            cart['canastas'] = []
    return cart


def agregar_producto_carrito(request, product_id, quantity):
    product = Catalogo_Producto.objects.get(id=product_id)
    cantidad_disponible = cantidad_disponible_producto_catalogo(product)
    cart = get_or_create_cart(request)

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


def agregar_canasta_carrito(request, canasta):
    cart = get_or_create_cart(request)
    canastas = cart.get('canastas', [])

    exists = False
    i = 0
    while not exists and i < len(canastas):
        canasta_act = canastas[i]
        if canasta_act['id'] == canasta.id:
            exists = True
            canasta_act['cantidad'] += 1
        i += 1

    if not exists:
        canastas.append({
            'id': canasta.id,
            'cantidad': 1,
            'canasta': canasta.to_dict
        })
    cart['canastas'] = canastas
    return cart
