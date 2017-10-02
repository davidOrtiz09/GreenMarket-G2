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