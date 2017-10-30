from MarketPlace.models import Productor, Cliente
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
