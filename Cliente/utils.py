from MarketPlace.models import Catalogo_Producto, Canasta, Oferta_Producto
from MarketPlace.utils import cantidad_disponible_producto_catalogo, get_or_create_week, get_id_cooperativa_global, cantidad_disponible_canasta
from django.db.models import F


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


def actualizar_inventario(producto_catalogo, cantidad):
    cantidad_restante = cantidad
    ofertas_productos = Oferta_Producto.objects \
        .filter(fk_producto=producto_catalogo.fk_producto, fk_oferta__fk_semana=get_or_create_week(), estado=1) \
        .exclude(cantidad_vendida=F('cantidad_aceptada')) \
        .order_by('precioProvedor')

    for oferta_producto in ofertas_productos:
        disponible_productos = oferta_producto.cantidad_aceptada - oferta_producto.cantidad_vendida
        if cantidad_restante == 0:
            break
        if disponible_productos >= cantidad_restante:
            oferta_producto.cantidad_vendida += cantidad_restante
            cantidad_restante = 0
        else:
            cantidad_restante -= disponible_productos
            oferta_producto.cantidad_vendida += disponible_productos
        oferta_producto.save()
    return cantidad_restante
