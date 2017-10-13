# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Cooperativa(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre de la Cooperativa', null=False, blank=False)
    ciudad = models.CharField(max_length=150, verbose_name='Ciudad de la Cooperativa', null=False, blank=False)
    departamento = models.CharField(max_length=150, verbose_name='Departamento de la Cooperativa', null=False,
                                    blank=False)

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
    fk_cooperativa = models.ForeignKey(Cooperativa, verbose_name='Cooperativa del productor', null=False,
                                       blank=False)
    nombre = models.CharField(max_length=150, verbose_name='Nombre del Productor', null=False, blank=False)
    direccion = models.CharField(max_length=150, verbose_name='Direccion del Productor ', null=False, blank=False)
    descripcion = models.TextField(max_length=150, verbose_name='Descripcion del Productor', null=False,
                                   blank=False)
    coordenadas_gps = models.CharField(max_length=150, verbose_name='Ubicación del Productor', null=False,
                                       blank=False)

    class Meta:
        verbose_name = 'Productor'
        verbose_name_plural = 'Productores'

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    descripcion = models.TextField(max_length=300, verbose_name='Descripción', null=False, blank=False)
    imagen = models.ImageField(upload_to='imagenes-categoria', verbose_name='Imagen', null=False, blank=False)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    UNIDAD_MEDIDA = (
        ('Kg', 'Kilogramos'),
        ('ud', 'Unidad')
    )

    fk_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría', null=False,
                                     blank=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    descripcion = models.TextField(max_length=300, verbose_name='Descripción', null=False, blank=False)
    imagen = models.ImageField(upload_to='imagenes-producto', verbose_name='Imagen', null=False, blank=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    unidad_medida = models.CharField(max_length=50, verbose_name='Unidad de medida', null=False, choices=UNIDAD_MEDIDA)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Oferta(models.Model):
    fk_productor = models.ForeignKey(Productor, verbose_name='Productor de la oferta', null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False, null=False,
                                 blank=False)

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'

    def __str__(self):
        return '{0}'.format(self.id)


@python_2_unicode_compatible
class Oferta_Producto(models.Model):
    fk_oferta = models.ForeignKey(Oferta, verbose_name='Oferta del Producto', null=False, blank=False)
    fk_producto = models.ForeignKey(Producto, verbose_name='Producto', null=False, blank=False)
    cantidad_ofertada = models.PositiveIntegerField(verbose_name='Cantidad ofertada del producto', null=False,
                                                    blank=False)
    cantidad_aceptada = models.PositiveIntegerField(verbose_name='Cantidad aceptada del producto', null=True,
                                                    blank=False, default=0)
    cantidad_vendida = models.PositiveIntegerField(verbose_name='Cantidad productos vendidos', null=False, blank=False,
                                                   default=0)
    fecha_aceptacion = models.DateTimeField(verbose_name='Fecha de aceptación de la oferta', null=True, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion de la oferta', null=True,
                                          blank=False)
    precioProvedor = models.FloatField(verbose_name='Precio del producto', null=False, blank=False)
    estado = models.SmallIntegerField(verbose_name='Estado de la oferta', null=False, blank=False, default=0)

    class Meta:
        verbose_name = 'Oferta de productos'
        verbose_name_plural = 'Ofertas de Productos'

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


class Catalogo_Producto(models.Model):
    fk_catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE, verbose_name='Catálogo', null=False,
                                    blank=False)
    fk_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto', null=False,
                                    blank=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Producto del Catalogo'
        verbose_name_plural = 'Productos del Catalogo'

    def __str__(self):
        return '{0}'.format(self.id)


class Cliente(models.Model):
    TIPO_DOCUMENTOS = (
        ('CC', 'Cédula de Ciudadanía'),
        ('PA', 'Pasaporte'),
        ('CE', 'Cédula de Extranjería'),
        ('RC', 'Registro Civil')
    )

    DEPARTAMENTOS = (
        ('1', 'Cundinamarca'),
        ('2', 'Boyaca'),
        ('3', 'Santander'),
        ('4', 'Bolívar')
    )

    CIUDADES = (
        ('1', 'Bogota'),
        ('2', 'Tunja'),
        ('3', 'Bucaramanga'),
        ('4', 'Cartagena')
    )

    # TODO: Cargar ciudades y departamentos
    fk_django_user = models.OneToOneField(User, verbose_name='Usuario tipo cliente', null=False, blank=False)
    departamento = models.CharField(max_length=2, choices=DEPARTAMENTOS)
    ciudad = models.CharField(max_length=2, choices=CIUDADES)
    numero_identificacion = models.CharField(max_length=20)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_DOCUMENTOS)
    telefono_contacto = models.CharField(max_length=15, null=False, blank=False)
    direccion = models.CharField(max_length=150, null=False, blank=False)

    class Meta:
        pass
        # unique_together = ('numero_identificacion', 'tipo_identificacion',)


class Pedido(models.Model):
    ESTADOS = (
        ('PE', 'PEDIDO'),
        ('EC', 'EN CAMINO'),
        ('EN', 'ENTREGADO')

    )
    fk_cliente = models.ForeignKey(Cliente, verbose_name='Cliente', null=False, blank=False)
    fecha_pedido = models.DateField(verbose_name='Fecha pedido', null=False, blank=False)
    fecha_entrega = models.DateField(verbose_name='Fecha de entrega del pedido', null=False, blank=False)
    estado = models.CharField(max_length=50, verbose_name='Estado', null=False, blank=False, choices=ESTADOS)
    valor_total = models.CharField(max_length=300, verbose_name='Valor del pedido', null=False, blank=False)


class PedidoProducto(models.Model):
    cantidad = models.IntegerField(default=0, blank=True, null=True)
    fk_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Producto', null=False, blank=False)
    fk_catalogo_producto = models.ForeignKey(Catalogo_Producto, on_delete=models.CASCADE,
                                             verbose_name='CatalogoProducto', null=False, blank=False)
