# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import calendar
from MarketPlace.models import Pedido, PedidoProducto, catalogo_producto, Producto


class Index(View):
    def get(self, request):
        return render(request, 'Administrador/index.html', {})

def pedidos(request):

    if request.method == 'POST':
        if request.POST.get('fechaInicio', '')=='':
            fechaInicio = datetime.now()
            fechaFin = datetime.now()
            listPedidos = Pedido.objects.filter(fecha_pedido__gte=fechaInicio, fecha_pedido__lte=fechaFin)
        else:
            fechaInicio = request.POST.get('fechaInicio', '')
            fechaFin = request.POST.get('fechaFin','')
            listPedidos = Pedido.objects.filter(fecha_pedido__gte=fechaInicio, fecha_pedido__lte=fechaFin)
    else:
        listPedidos = Pedido.objects.all()
    context = {'listPedidos': listPedidos}
    return render(request, 'administrador/pedidos.html', context)

def detallePedido(request, id_pedido):
    listDetallePedido = PedidoProducto.objects.filter(fk_pedido=id_pedido)
    pedido=Pedido.objects.get(id=id_pedido)
    if pedido.estado != 'PE':
        disableButton = 'disabled'
    else:
        disableButton = ''
    context = {'listDetallePedido':listDetallePedido, 'id_pedido':id_pedido,'disableButton':disableButton }
    return render(request, 'administrador/detallePedidos.html', context)

def actualizarEstadoPedido (request, id_pedidoUpdate):
    pedidoUpdate=Pedido.objects.get(id=id_pedidoUpdate)
    pedidoUpdate.estado = 'EC'
    pedidoUpdate.save()
    listPedidos = Pedido.objects.all()
    context = {'listPedidos': listPedidos}
    return render(request, 'administrador/pedidos.html', context)


