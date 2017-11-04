# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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
