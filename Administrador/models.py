# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class MejoresClientes:
    def __init__(self, cliente_id, nombre, cantidad_comprada, total_compras, ultima_fecha_de_compra):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.cantidad_comprada = cantidad_comprada
        self.total_compras = total_compras
        self.ultima_fecha_de_compra = ultima_fecha_de_compra


class ProductorDestacado:
    def __init__(self, productor_id, nombre, cooperativa, total_ventas, ultima_fecha_de_venta):
        self.productor_id = productor_id
        self.nombre = nombre
        self.cooperativa = cooperativa
        self.total_ventas = total_ventas
        self.ultima_fecha_de_venta = ultima_fecha_de_venta

class ProductosSugeridos:
    def __init__(self, productor_id, nombre, imagen, unidad_medida, cantidad, num_usuarios):
        self.productor_id = productor_id
        self.nombre = nombre
        self.imagen = imagen
        self.unidad_medida = unidad_medida
        self.cantidad = cantidad
        self.num_usuarios=num_usuarios


class Ciudad:
    def __init__(self, valor, nombre):
        self.valor = valor
        self.nombre = nombre

    @staticmethod
    def get_all_ciudades():
        return [Ciudad(1, 'Bogota'),   Ciudad(2, 'Tunja'),   Ciudad(3, 'Bucaramanga'), Ciudad(4, 'Cartagena')]


class Departamento:
    def __init__(self, valor, nombre):
        self.valor = valor
        self.nombre = nombre

    @staticmethod
    def get_all_departamentos():
        return [Departamento(1, 'Cundinamarca'),   Departamento(2, 'Boyaca'),   Departamento(3, 'Santander'), Departamento(4, 'Bolívar')]
