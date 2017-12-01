import datetime
from MarketPlace.models import Productor, Cliente, Semana, Cooperativa, Oferta_Producto
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse


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


def get_or_create_prev_week():
    today = datetime.date.today()
    a_week_ago = today - datetime.timedelta(weeks=1)
    existe = Semana.objects.filter(fecha_inicio__lte=a_week_ago, fecha_fin__gte=a_week_ago).first()
    if existe:
        return existe
    else:
        that_monday = a_week_ago - datetime.timedelta(days=a_week_ago.weekday())
        that_sunday = that_monday + datetime.timedelta(weeks=1) - datetime.timedelta(days=1)
        nueva = Semana(
            fk_cooperativa_id=Cooperativa.objects.first().id,
            fecha_inicio=that_monday,
            fecha_fin=that_sunday
        )
        nueva.save()
        return nueva


def cantidad_disponible_producto_catalogo(producto_catalogo, cooperativa_id):
    response = 0
    ofertas_producto = Oferta_Producto.objects.filter(
        fk_producto_id=producto_catalogo.fk_producto_id,
        fk_oferta__fk_semana_id=get_or_create_week().id,
        fk_oferta__fk_productor__fk_cooperativa_id=cooperativa_id
    )
    for oferta_producto in ofertas_producto:
        response += oferta_producto.cantidad_aceptada - oferta_producto.cantidad_vendida
    return response

def formatear_lista_productos(productos_catalogo, request ,cooperativa_id):
    productos = []
    for producto in productos_catalogo:
        cantidad_disponible = cantidad_disponible_producto_catalogo(producto, cooperativa_id)
        if cantidad_disponible > 0:
            product_dict = producto.to_dict(request.user)
            product_dict['cantidad_disponible'] = cantidad_disponible
            productos.append(product_dict)

    return productos