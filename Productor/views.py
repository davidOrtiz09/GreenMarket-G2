# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from django.db.models.expressions import F
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from MarketPlace.models import Oferta_Producto, Producto, Productor, Oferta, Categoria


class Ingresar(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('productor:index'))
        else:
            return render(request, 'Productor/ingresar.html', {})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('productor:index'))
        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('productor:index'))
            else:
                messages.add_message(request, messages.ERROR, 'Por favor verifica tu usuario y contraseña')
                return render(request, 'Productor/ingresar.html', {})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('productor:ingresar'))


class Index(View):
    def get(self, request):
        return render(request, 'Productor/crear_oferta.html', {})


class ProductosVendidosView(View):
    def get(self, request):

        dia_semana = datetime.date.today().weekday()

        # Si el dia esta entre el jueves y el domingo.
        if dia_semana >= 3:
            dias_restar = dia_semana -3
        else:
            dias_restar = dia_semana + 4

        # Por el momento se toma el primer productor que devuelve la consulta.
        productor = Productor.objects.first()

        # Se obtienen las ofertas  realizadas por un productor y que fueron aceptadas
        # Solo se toman las ofertas de realizadas desde el día actual al jueves anterior.
        ofertas_pro = Oferta_Producto \
            .objects.filter(estado=1, fk_oferta__fk_productor=productor ,
                            fk_oferta__fecha__gte=datetime.date.today() + datetime.timedelta(days=-dias_restar)) \
            .values('fk_producto__nombre', 'fk_producto__unidad_medida', 'cantidad_aceptada',
                    'cantidad_vendida', 'precioProvedor', cantidad_disponible= F('cantidad_aceptada') - F('cantidad_vendida'))


        hay_ofertas = ofertas_pro.count() > 0

        if hay_ofertas:
            subtitulo = datetime.date.today().strftime("%d/%m/%y")
        else:
            subtitulo = "No hay ofertas aceptadas para la semana"

        return render(request, 'Productor/productos_vendidos.html'
                      ,{'ofertas_pro':ofertas_pro, 'hay_ofertas':hay_ofertas, 'subtitulo':subtitulo})


def crear_oferta(request):
    context = {
        'form': 'form'
    }
    return render(request, 'Productor/crear_oferta.html', context)


def get_categorias_view(request):
    categorias = Categoria.objects.all().values('nombre','id')
    context = {"ListaCategorias":list(categorias)}
    return JsonResponse(context)


def get_productos_por_categoria(request):
    idCategoria = request.GET['idCategoria']
    productos = Producto.objects.filter(fk_categoria_id = idCategoria).values('nombre','id','unidad_medida')
    context = {"ListaProductos":list(productos)}
    return JsonResponse(context)

@csrf_exempt
def agregar_oferta_productor(request):
    context = {}
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        productor = Productor.objects.all().first()
        oferta = Oferta(fk_productor = productor)
        oferta.save()
        for producto in  body:
            productoObjeto = Producto.objects.filter(id=producto["idProducto"]).first()
            ofertaProducto = Oferta_Producto(fk_oferta = oferta, fk_producto = productoObjeto,
                                             cantidad_ofertada = producto["TotalProductos"], precioProvedor = producto["Precio"])
            ofertaProducto.save()
        context = {"Mensaje":"Finalizó con exito"}
    return JsonResponse(context)