# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from MarketPlace.models import Catalogo, Producto,CatalogoProducto, Categoria,Cooperativa


class Index(View):
    def get(self, request):
        cooperativas = Cooperativa.objects.all()
        producto_catalogo=CatalogoProducto.objects.filter(fk_catalogo__fk_cooperativa__nombre__exact=cooperativas[0])\
                .order_by('fk_producto__nombre')
        categorias = Categoria.objects.all()
        context = {'productos_catalogo': producto_catalogo, 'categorias': categorias,
                   'cooperativas': cooperativas}
        return render(request, 'Cliente/index.html', context)

    def post(self, request):
        #Se listan los productos por Cooperativa y se ordenan segun filtro
        cooperativa = request.POST.get('cooperativa', '')
        ordenarPor = request.POST.get('ordenar', '')
        producto_catalogo = CatalogoProducto.objects.filter(fk_catalogo__fk_cooperativa__nombre__exact=cooperativa)\
            .order_by(ordenarPor)
        categorias = Categoria.objects.all()
        cooperativas = Cooperativa.objects.all()
        context = {'productos_catalogo': producto_catalogo, 'categorias': categorias,
                   'cooperativas': cooperativas}
        return render(request, 'Cliente/index.html', context)




