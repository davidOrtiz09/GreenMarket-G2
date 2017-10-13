# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from MarketPlace.models import Categoria, Producto, Oferta, Oferta_Producto, Cooperativa, Productor, Pedido, Cliente, \
    Catalogo, Catalogo_Producto, PedidoProducto


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre',)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre',)


class OfertaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_productor', 'fecha')
    list_display_links = ('id',)
    search_fields = ('nombre',)


class Oferta_ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_oferta', 'fk_producto', 'estado', 'cantidad_aceptada', 'cantidad_vendida', 'precioProvedor')
    list_display_links = ('id',)
    search_fields = ('estado',)


class CooperativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'departamento')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre',)


class ProductorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre',)


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Oferta_Producto, Oferta_ProductoAdmin)
admin.site.register(Cooperativa, CooperativaAdmin)
admin.site.register(Productor, ProductorAdmin)
admin.site.register(Pedido)
admin.site.register(Cliente)
admin.site.register(Catalogo)
admin.site.register(Catalogo_Producto)
admin.site.register(PedidoProducto)
