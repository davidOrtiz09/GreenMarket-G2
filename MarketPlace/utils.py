import datetime
from MarketPlace.models import Productor, Cliente, Semana, Cooperativa, Oferta_Producto, ClienteProducto
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse
from django.db.models import F

def es_productor(usuario):
    return Productor.objects.filter(fk_django_user_id=usuario.id).exists()


def es_cliente(usuario):
    return Cliente.objects.filter(fk_django_user_id=usuario.id).exists()


def es_administrador(usuario):
    return usuario.is_staff


def redirect_user_to_home(request):
    if es_productor(request.user):
        return redirect(reverse('productor:index'))
    elif es_cliente(request.user):
        return redirect(reverse('cliente:index'))
    elif es_administrador(request.user):
        return redirect(reverse('administrador:index'))
    else:
        logout(request)
        return redirect(reverse('cliente:index'))


def get_or_create_week():
    today = datetime.date.today()
    existe = Semana.objects.filter(fecha_inicio__lte=today, fecha_fin__gte=today).first()
    if existe:
        return existe
    else:
        prev_monday = today - datetime.timedelta(days=today.weekday())
        next_sunday = prev_monday + datetime.timedelta(weeks=1) - datetime.timedelta(days=1)
        nueva = Semana(
            fecha_inicio=prev_monday,
            fecha_fin=next_sunday
        )
        nueva.save()
        sugerir_productos()
        return nueva


def get_or_create_next_week():
    today = datetime.date.today()
    next_week = today + datetime.timedelta(weeks=1)
    existe = Semana.objects.filter(fecha_inicio__lte=next_week, fecha_fin__gte=next_week).first()
    if existe:
        return existe
    else:
        prev_monday = next_week - datetime.timedelta(days=next_week.weekday())
        next_sunday = prev_monday + datetime.timedelta(weeks=1) - datetime.timedelta(days=1)
        nueva = Semana(
            fecha_inicio=prev_monday,
            fecha_fin=next_sunday
        )
        nueva.save()
        return nueva


def cantidad_disponible_producto_catalogo(producto_catalogo, cooperativa_id):
    response = 0
    ofertas_producto = Oferta_Producto.objects.filter(
        fk_producto_id=producto_catalogo.fk_producto_id,
        fk_oferta__fk_semana_id=get_or_create_week().id,
        fk_oferta__fk_productor__fk_cooperativa_id=cooperativa_id
    ).exclude(cantidad_vendida=F('cantidad_aceptada'))
    for oferta_producto in ofertas_producto:
        response += oferta_producto.cantidad_aceptada - oferta_producto.cantidad_vendida
    return response


def cantidad_disponible_canasta(canasta, cooperativa_id):
    response = -1

    for producto_canasta in canasta.productos:
        cantidad_producto_individual = cantidad_disponible_producto_catalogo(producto_canasta.fk_producto_catalogo, cooperativa_id)
        cantidad_producto = cantidad_producto_individual / producto_canasta.cantidad
        if response == -1:
            response = cantidad_producto
        elif cantidad_producto < response:
            response = cantidad_producto

    return response


def number_to_cop(number):
    try:
        return format(number, ',.0f')
    except Exception as e:
        return number


def formatear_lista_productos(productos_catalogo, request, cooperativa_id):
    productos = []
    for producto in productos_catalogo:
        cantidad_disponible = cantidad_disponible_producto_catalogo(producto, cooperativa_id)
        if cantidad_disponible > 0:
            product_dict = producto.to_dict(request.user)
            product_dict['cantidad_disponible'] = cantidad_disponible
            productos.append(product_dict)

    return productos


def formatear_lista_canastas(canastas_catalogo, cooperativa_id):
    canastas = []
    for canasta in canastas_catalogo:
        cantidad_disponible = cantidad_disponible_canasta(canasta, cooperativa_id)
        if cantidad_disponible > 0:
            canasta_dict = canasta.to_dict
            canasta_dict['cantidad_disponible'] = cantidad_disponible
            canastas.append(canasta_dict)
    return canastas


def get_cooperativa_global(request):
    cooperativa = None
    if es_administrador(request.user):
        cooperativa = request.session.get('cooperativa', None)

    if cooperativa is None:
        cooperativa = Cooperativa.objects.first().to_json()

    return cooperativa


def get_id_cooperativa_global(request):
    return get_cooperativa_global(request)['id']


def sugerir_productos():
    ClienteProducto.objects.update(sugerir=False)
    ofertas_productos=Oferta_Producto.objects.filter(fk_oferta__fk_semana=get_or_create_week(), cantidad_aceptada__gt=0)\
        .distinct('fk_producto')

    for oferta_producto in ofertas_productos:
        cliente_producto_id = ClienteProducto.objects.filter(fk_producto=oferta_producto.fk_producto)\
            .order_by('cantidad').values('id')[:10]
        ClienteProducto.objects.filter(id__in=cliente_producto_id).update(sugerir=True)
