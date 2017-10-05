# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


class Index(View):
    def get(self, request):
        return render(request, 'Cliente/index.html', {})


class CarritoDeCompras(View):
    def get(self, request):
        return render(request, 'Cliente/carrito-de-compras.html', {})
