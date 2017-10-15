# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models.expressions import ExpressionWrapper, F
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from MarketPlace.models import Oferta_Producto, Catalogo, Producto, Pedido, PedidoProducto, Catalogo_Producto, \
    Productor, Oferta, Cooperativa


class Index(View):
    def get(self, request):
        return render(request, 'Productor/crear_oferta.html', {})


class ProductosVendidosView(View):
    def get(self, request):

        dia_semana = datetime.date.today().weekday()

        # Si el dia esta entre el jueves y el domingo.
        if (dia_semana >= 3):
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
