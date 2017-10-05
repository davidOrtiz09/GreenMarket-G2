# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum, Min, Max
from django.shortcuts import render
from django.views import View
from MarketPlace.models import Oferta, Oferta_Producto, Producto
from django.http import JsonResponse


class Index(View):
    def get(self, request):
        return render(request, 'Administrador/index.html', {})

class Catalogo(View):
    def get(self, request):

        ofertas_pro = Oferta_Producto.objects.values('fk_producto', 'fk_producto__nombre', 'fk_producto__imagen').annotate(
            preMin=Min('precioProvedor'), preMax=Max('precioProvedor'), canAceptada=Sum('cantidad_aceptada')).distinct()
        #print(aqui)
        return render(request, 'Administrador/catalogo.html', {'ofertas_pro':ofertas_pro})
