# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from MarketPlace.models import Catalogo, Producto,CatalogoProducto


class Index(View):
    def get(self, request):
        catalogo_producto=CatalogoProducto.objects.all()
        context = {'productos_catalogo': catalogo_producto}
        return render(request, 'Cliente/index.html', context)

