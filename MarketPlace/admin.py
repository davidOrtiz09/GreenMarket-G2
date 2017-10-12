# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from MarketPlace.models import Pedido
from MarketPlace.models import Cliente
from MarketPlace.models import Catalogo
from MarketPlace.models import Categoria
from MarketPlace.models import Producto
from MarketPlace.models import catalogo_producto
from MarketPlace.models import PedidoProducto
from django.contrib import admin

# Register your models here.

admin.site.register(Pedido)
admin.site.register(Cliente)
admin.site.register(Catalogo)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(catalogo_producto)
admin.site.register(PedidoProducto)
