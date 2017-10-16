# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from MarketPlace.models import Categoria, Producto, Oferta, Oferta_Producto, Productor


class Index(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'})


def crear_oferta(request):
    context = {
        'form': 'form'
    }
    return render(request, 'crear_oferta.html', context)


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