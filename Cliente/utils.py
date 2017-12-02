from MarketPlace.models import Catalogo_Producto, Canasta
from MarketPlace.utils import cantidad_disponible_producto_catalogo, get_or_create_week, get_id_cooperativa_global, cantidad_disponible_canasta


def get_or_create_cart(request):
    cart = request.session.get('cart', None)
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
    product = Catalogo_Producto.objects.get(fk_producto_id=product_id,
                                            fk_catalogo__fk_cooperativa_id=get_id_cooperativa_global(request),
                                            fk_catalogo__fk_semana=get_or_create_week())
    cantidad_disponible = cantidad_disponible_producto_catalogo(product, get_id_cooperativa_global(request))
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


def agregar_canasta_carrito(request, canasta_id, quantity):
    canasta = Canasta.objects.get(id=canasta_id)
    cantidad_disponible = cantidad_disponible_canasta(canasta, get_id_cooperativa_global(request))
    cart = get_or_create_cart(request)
    canastas = cart.get('canastas', [])
    exists = False
    i = 0
    while not exists and i < len(canastas):
        canasta_act = canastas[i]
        if canasta_act['id'] == canasta_id:
            new_quantity = canasta_act['quantity'] + quantity
            if new_quantity > cantidad_disponible:
                new_quantity = cantidad_disponible
            canasta_act['quantity'] = new_quantity
            exists = True
        i += 1
    if not exists:
        canastas.append({
            'id': canasta_id,
            'quantity': quantity,
            'name': canasta.nombre,
            'image': canasta.imagen.url if canasta.imagen else '',
            'price': float(canasta.precio),
            'cantidad_disponible': cantidad_disponible
        })
    cart['canastas'] = canastas
    return cart
