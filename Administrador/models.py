# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class MejoresClientes:
    def __init__(self, cliente_id, nombre, cantidad_comprada, total_compras, ultima_fecha_de_compra):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.cantidad_comprada = cantidad_comprada
        self.total_compras = total_compras
        self.ultima_fecha_de_compra = ultima_fecha_de_compra
