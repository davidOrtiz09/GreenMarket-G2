# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from django.db.models import Sum, Min, Max
from django.shortcuts import render
from django.views import View
from MarketPlace.models import Oferta_Producto, Catalogo, catalogo_producto, Producto
from Administrador.utils import catalogo_actual


class Index(View):
    def get(self, request):
        return render(request, 'Administrador/index.html', {})


class CatalogoView(View):
    def get(self, request):
        dia_semana = datetime.date.today().weekday()
        oferta_nueva = False
        info_catalogo = {}
        # Se valida que sea domingo para permitir crear el catalogo.
        if dia_semana == 6:
            # Se valida que no se haya creado ya un catalogo para la semana.
            catalogo = Catalogo.objects.filter(fecha_creacion__gte=datetime.date.today()).first()
            if catalogo is None:
                # Se obtienen las ofertas agrupadas por producto (cantidad, precio minimo y maximo)
                # Solo se toman las ofertas de los 3 dias anteriores(jueves, viernes, sabado)
                ofertas_pro = Oferta_Producto\
                    .objects.filter(estado=1, fk_oferta__fecha__gte=datetime.date.today() + datetime.timedelta(days=-3))\
                    .values('fk_producto', 'fk_producto__nombre', 'fk_producto__imagen')\
                    .annotate(preMin=Min('precioProvedor'), preMax=Max('precioProvedor'), canAceptada=Sum('cantidad_aceptada'))\
                    .distinct()

                oferta_nueva = ofertas_pro.count() > 0

                if oferta_nueva:
                    subtitulo = datetime.date.today().strftime("%d/%m/%y")
                else:
                    subtitulo = "No hay ofertas disponibles para crear el catálogo"

                info_catalogo.update({'ofertas_pro': ofertas_pro, 'subtitulo': subtitulo})
            else:
                # Se muestra el catalogo ya creado.
                info_catalogo = catalogo_actual()
        else:
            # Si no es domingo se muestra el ultimo catalogo que se haya creado.
            info_catalogo = catalogo_actual()

        return render(request, 'Administrador/catalogo.html',
                      {'ofertas_pro': info_catalogo['ofertas_pro'],
                       'subtitulo':info_catalogo['subtitulo'],
                       'oferta_nueva': oferta_nueva})

    def post(self, request):
        # Se carga la información desde el JSON recibido donde viene el id del producto con su respectivo precio.
        precios_recibidos = json.loads(request.POST.get('precios_enviar'))

        # Se crea el catalogo
        fecha_cierre = datetime.date.today() + datetime.timedelta(days=3)
        catalogo = Catalogo.objects.create(productor_id=1, fecha_cierre=fecha_cierre)
        catalogo.save()

        # Se agregan los  productos al catalogo
        for item in precios_recibidos:
            catalogo_producto.objects.create(fk_catalogo=catalogo,
                                             fk_producto=Producto(id=item['producto']),
                                             precio=item['precio'])

        # Se carga la informacion del catalogo creado
        info_catalogo = catalogo_actual()
        subtitulo = "Catálogo creado correctamente!\r\n" + info_catalogo['subtitulo']

        return render(request, 'Administrador/catalogo.html', {
            'ofertas_pro': info_catalogo['ofertas_pro'],
            'subtitulo': subtitulo,
            'oferta_nueva': False
        })

