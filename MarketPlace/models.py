# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Catalogo(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion=models.DateField(auto_now_add=True)
    fecha_cierre = models.DateTimeField()
    nombre = models.CharField(max_length=100, verbose_name='Pais', null=False, blank=False)
    class Meta:
        verbose_name = 'Catalogo'
        verbose_name_plural = 'Catalagos'

    def __str__(self):
        return self.name


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion=models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    descripcion= models.TextField(max_length=1000, verbose_name='Descripción', null=True, blank=True)
    imagen= models.ImageField(upload_to='user-pictures', verbose_name='Foto', null=True, blank=False)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    categoria=models.CharField(max_length=50, verbose_name='Categoría', null=False, blank=False)
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name


class CatalogoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    precio=models.DecimalField(max_digits=10, decimal_places=2)
    fk_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto', null=False, blank=False)
    fk_catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE, verbose_name='Catalogo', null=False, blank=False)
    class Meta:
        verbose_name = 'Producto del Catalogo'

    def __str__(self):
        return self.name




class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion=models.DateField(auto_now_add=True)
    fecha_hora_entrega = models.DateTimeField()
    estado=models.BooleanField()
    direccion_entrega = models.CharField(max_length=300, unique=False, null=False, blank=False)
    nombre_repartidor= models.CharField(max_length=300, unique=False, null=False, blank=False)
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return self.name


class PedidoProducto(models.Model):
    cantidad = models.IntegerField(default=0, blank=True, null=True)
    fk_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Producto', null=False, blank=False)
    fk_catalogo_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='CatalogoProducto', null=False, blank=False)

    class Meta:
        unique_together = ("fk_pedido", "fk_catalogo_producto")

    def __str__(self):
        return self.name
