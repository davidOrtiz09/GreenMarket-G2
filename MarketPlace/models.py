# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import defaultdict
from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Cooperativa(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre de la Cooperativa', null=False, blank=False)
    ciudad = models.CharField(max_length=150, verbose_name='Ciudad de la Cooperativa', null=False, blank=False)
    departamento = models.CharField(max_length=150, verbose_name='Departamento de la Cooperativa', null=False, blank=False)

    class Meta:
        verbose_name = 'Cooperativa'
        verbose_name_plural = 'Cooperativas'

    def __str__(self):
        return self.nombre

    def to_json(self):
        return {
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "departamento": self.departamento,
            "id": self.id
        }

@python_2_unicode_compatible
class Productor(models.Model):
    fk_cooperativa = models.ForeignKey(Cooperativa, verbose_name='Cooperativa del productor', null=False, blank=False)
    nombre = models.CharField(max_length=150, verbose_name='Nombre del Productor', null=False, blank=False)
    direccion = models.CharField(max_length=150, verbose_name='Direccion del Productor ', null=False, blank=False)
    descripcion = models.TextField(max_length=150, verbose_name='Descripcion del Productor', null=False, blank=False)
    coordenadas_gps = models.CharField(max_length=150, verbose_name='Ubicación del Productor', null=False, blank=False)

    class Meta:
        verbose_name = 'Productor'
        verbose_name_plural = 'Productores'

    def __str__(self):
        return self.nombre



@python_2_unicode_compatible
class Oferta(models.Model):
    fk_productor= models.ForeignKey(Productor, verbose_name='Productor de la oferta', null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False, null=False, blank=False)

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'

    def __str__(self):
        return '{0}'.format(self.id)


@python_2_unicode_compatible
class Producto(models.Model):
    fk_categoria = models.ForeignKey(Categoria, verbose_name='Categoria del producto', null=False, blank=False)
    nombre = models.CharField(max_length=150, verbose_name='Nombre del Producto', null=False, blank=False)
    descripcion = models.TextField(max_length=150, verbose_name='Descripcion del Producto', null=False, blank=False)
    url_foto = models.CharField(max_length=150, verbose_name='Foto del Producto', null=False, blank=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre

@python_2_unicode_compatible
class Categoria(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre de la categoria', null=False, blank=False)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Oferta_Producto(models.Model):
    fk_oferta = models.ForeignKey(Oferta, verbose_name='Oferta del Producto', null=False, blank=False)
    fk_producto= models.ForeignKey(Producto, verbose_name='Producto', null=False, blank=False)
    cantidad_ofertada = models.PositiveIntegerField(verbose_name='Cantidad ofertada del producto', null=False, blank=False)
    cantidad_aceptada = models.PositiveIntegerField(verbose_name='Cantidad aceptada del producto', null=True, blank=False, default=0)
    cantidad_vendida = models.PositiveIntegerField(verbose_name='Cantidad productos vendidos', null=False, blank=False, default=0)
    fecha_aceptacion = models.DateTimeField(verbose_name='Fecha de aceptación de la oferta',  null=True, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion de la oferta', null=True, blank=False)
    precioProvedor = models.FloatField(verbose_name='Precio del producto', null=False, blank=False)
    estado = models.SmallIntegerField(verbose_name='Estado de la oferta', null=False, blank=False, default=0)


    class Meta:
        verbose_name = 'Oferta de productos'
        verbose_name_plural = 'Ofertas de Productos'

    def __str__(self):
        return '{0}'.format(self.id)



