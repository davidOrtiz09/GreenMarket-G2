# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from django.db.models import Sum, Min, Max
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from MarketPlace.models import Oferta_Producto, Catalogo, catalogo_producto, Producto
from django.http import JsonResponse


class Index(View):
    def get(self, request):
        return render(request, 'Administrador/index.html', {})

class CatalogoView(View):
    def get(self, request):
        # ofertas_pro = Oferta_Producto.objects.filter(estado=1, fk_oferta__fecha__gte=datetime.date.today()).values('fk_producto', 'fk_producto__nombre', 'fk_producto__imagen').annotate(
        ofertas_pro = Oferta_Producto.objects.filter(estado=1).values(
            'fk_producto', 'fk_producto__nombre', 'fk_producto__imagen').annotate(
            preMin=Min('precioProvedor'), preMax=Max('precioProvedor'), canAceptada=Sum('cantidad_aceptada')).distinct()
        # print(aqui)
        return render(request, 'Administrador/catalogo.html', {'ofertas_pro': ofertas_pro})

    def post(self, request):
        if (request.method == 'POST'):
            precios_recibidos = json.loads(request.POST.get('precios_enviar'))
            catalogo = Catalogo.objects.create(productor_id = 1,
                                               fecha_cierre = datetime.date.today() + datetime.timedelta(days=3))
            catalogo.save()
            for item in precios_recibidos:
                cat_pro = catalogo_producto.objects.create(fk_catalogo = catalogo,
                                                           fk_producto = Producto(id = item['producto']),
                                                           precio = item['precio'])
            return redirect(reverse('administrador:index'))
