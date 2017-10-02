# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    descripcion = models.TextField(max_length=300, verbose_name='Descripción', null=False, blank=False)
    imagen = models.ImageField(upload_to='imagenes-categoria', verbose_name='Imagen', null=False, blank=False)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    fk_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría', null=False, blank=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    descripcion = models.TextField(max_length=300, verbose_name='Descripción', null=False, blank=False)
    imagen = models.ImageField(upload_to='imagenes-producto', verbose_name='Imagen', null=False, blank=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class Oferta(models.Model):
    productor_id = models.IntegerField(null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'

    def __str__(self):
        return '{0}'.format(self.id)


class oferta_producto(models.Model):
    fk_oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, verbose_name='Oferta', null=False, blank=False)
    fk_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto', null=False, blank=False)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de Creación", null=False, blank=False, auto_now_add=True)
    fecha_aceptacion = models.DateTimeField(verbose_name="Fecha de Aceptación", null=True)
    precio = models.FloatField(verbose_name="Precio", null=False, blank=False)
    cantidad_ofertada = models.IntegerField(verbose_name="Cantidad Ofertada", null=False, blank=False)
    cantidad_aceptada = models.IntegerField(verbose_name="Cantidad Aceptada", null=False, blank=False, default=0)
    cantidad_vendida = models.IntegerField(verbose_name="Cantidad Vendida", null=False, blank=False, default=0)
    estado = models.SmallIntegerField(verbose_name="Estado", null=False, blank=False)

    class Meta:
        verbose_name = 'Oferta de producto'
        verbose_name_plural = 'Ofertas de producto'

    def __str__(self):
        return '{0}'.format(self.id)

class Catalogo(models.Model):
    productor_id = models.IntegerField(null=False, blank=False)
    fecha_creacion = models.DateField(verbose_name="Fecha de Creación", null=False, blank=False, auto_now_add=True)
    fecha_cierre = models.DateTimeField(verbose_name="Fecha de Cierre", null=False, blank=False)

    class Meta:
        verbose_name = 'Catálogo'
        verbose_name_plural = 'Catálogos'

    def __str__(self):
        return '{0}'.format(self.id)
