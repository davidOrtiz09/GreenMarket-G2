# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from decimal import Decimal
from MarketPlace.templatetags.marketplace_filters import to_cop


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
    fk_django_user = models.OneToOneField(User, verbose_name='Usuario tipo productor', null=False, blank=False)
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


class Orden_Compra(models.Model):
    ESTADOS = (
        ('PP', 'Por Pagar'),
        ('PA', 'Pago'),
        ('AC', 'Activo'),
        ('CA', 'Cancelado')

    )
    fecha_pago = models.DateField(verbose_name='Fecha pago', null=False, blank=False,auto_now_add=True)
    fecha_creacion = models.DateField(verbose_name='Fecha Creacion', null=False, blank=False,auto_now_add=True)
    fk_productor = models.ForeignKey(Productor, on_delete=models.CASCADE, verbose_name='Productor', null=False, blank=False)
    estado = models.CharField(max_length=2, verbose_name='Estado', null=False, blank=False, choices=ESTADOS)
    valor_total = models.DecimalField(verbose_name='Precio Total', null=False, blank=False, max_digits=10, decimal_places=2,default=0.0)
    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Ordenes de Compra'


@python_2_unicode_compatible
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    descripcion = models.TextField(max_length=300, verbose_name='Descripción', null=False, blank=False)
    imagen = models.ImageField(upload_to='imagenes-categoria', verbose_name='Imagen', null=False, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

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
class Semana(models.Model):
    fk_cooperativa = models.ForeignKey(Cooperativa, verbose_name='Cooperativa', null=False,
                                       blank=False)
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio", null=False, blank=False)
    fecha_fin = models.DateField(verbose_name="Fecha Fin", null=False, blank=False)

    class Meta:
        verbose_name = 'Semana'
        verbose_name_plural = 'Semanas'

    def __str__(self):
        return 'de ' + self.fecha_inicio.__str__() + ' al ' + self.fecha_fin.__str__()


@python_2_unicode_compatible
class Oferta(models.Model):
    fk_semana = models.ForeignKey(Semana, verbose_name='Semana', null=False, blank=False)
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
    fk_orden_compra = models.ForeignKey(Orden_Compra, verbose_name='Orden de Compra', null=True, blank=True)
    cantidad_ofertada = models.PositiveIntegerField(verbose_name='Cantidad ofertada del producto', null=False,
                                                    blank=False)
    cantidad_aceptada = models.PositiveIntegerField(verbose_name='Cantidad aceptada del producto', null=True,
                                                    blank=False, default=0)
    cantidad_vendida = models.PositiveIntegerField(verbose_name='Cantidad productos vendidos', null=False, blank=False,
                                                   default=0)
    fecha_aceptacion = models.DateTimeField(verbose_name='Fecha de aceptación de la oferta', null=True, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion de la oferta', null=True,
                                          blank=False)
    precioProvedor = models.DecimalField(verbose_name='Precio del producto', null=False, blank=False, max_digits=10, decimal_places=2)
    estado = models.SmallIntegerField(verbose_name='Estado de la oferta', null=False, blank=False, default=0)

    class Meta:
        verbose_name = 'Oferta de productos'
        verbose_name_plural = 'Ofertas de Productos'

    def __str__(self):
        return '{0}'.format(self.id)

    @staticmethod
    def cargar_ofertas(id_oferta):
        ofertas_producto = list()
        for oferta in Oferta_Producto.objects.filter(fk_oferta=id_oferta):
            producto = oferta.fk_producto
            ofertas_producto.append(
                (producto.imagen.url, producto.nombre, oferta.cantidad_ofertada, oferta.precioProvedor,
                 oferta.cantidad_aceptada, oferta.estado, producto.unidad_medida, oferta.id))
        return ofertas_producto


@python_2_unicode_compatible
class Catalogo(models.Model):
    fk_semana = models.ForeignKey(Semana, verbose_name='Semana', null=False, blank=False)
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

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'id_producto': self.fk_producto_id,
            'descripcion': self.fk_producto.descripcion,
            'imagen': self.fk_producto.imagen.url if self.fk_producto.imagen else '',
            'precio': float(self.precio),
            'precio_cop': to_cop(float(self.precio)),
            'nombre': self.fk_producto.nombre,
            'unidad_medida': self.fk_producto.unidad_medida,
            'categoria': {
                'id': self.fk_producto.fk_categoria_id,
                'nombre': self.fk_producto.fk_categoria.nombre
            },
            'cantidad_carrito': 0
        }

    class Meta:
        verbose_name = 'Producto del Catalogo'
        verbose_name_plural = 'Productos del Catalogo'
        unique_together = (('fk_catalogo', 'fk_producto'),)

    def __str__(self):
        return '{0} (Catalogo {1})'.format(self.fk_producto.nombre, self.fk_catalogo_id)


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


@python_2_unicode_compatible
class Pedido(models.Model):
    TIPO_DOCUMENTOS = (
        ('CC', 'Cédula de Ciudadanía'),
        ('PA', 'Pasaporte'),
        ('CE', 'Cédula de Extranjería'),
        ('RC', 'Registro Civil')
    )
    ESTADOS = (
        ('PE', 'PEDIDO'),
        ('EC', 'EN CAMINO'),
        ('EN', 'ENTREGADO')

    )
    fk_cliente = models.ForeignKey(Cliente, verbose_name='Cliente', null=False, blank=False)
    fecha_pedido = models.DateField(verbose_name='Fecha pedido', null=False, blank=False)
    fecha_entrega = models.DateField(verbose_name='Fecha de entrega del pedido', null=False, blank=False)
    estado = models.CharField(max_length=50, verbose_name='Estado', null=False, blank=False, choices=ESTADOS)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    nombre_envio = models.CharField(max_length=150, verbose_name='Nombre', null=False, blank=False)
    direccion_envio = models.CharField(max_length=150, null=False, blank=False)
    email_envio = models.CharField(max_length=150, null=False, blank=False)
    telefono_envio = models.CharField(max_length=150, null=False, blank=False)
    observaciones_envio = models.CharField(max_length=150, null=False, blank=False)

    nombre_pago = models.CharField(max_length=150, null=False, blank=False)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_DOCUMENTOS)
    numero_identificacion = models.CharField(max_length=20)

    def __str__(self):
        return '{cliente} (Pedido {fecha})'.format(cliente=self.fk_cliente, fecha=self.fecha_pedido)


@python_2_unicode_compatible
class PedidoProducto(models.Model):
    cantidad = models.IntegerField(default=0, blank=True, null=True)
    fk_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Pedido', null=False, blank=False)
    fk_catalogo_producto = models.ForeignKey(Catalogo_Producto, on_delete=models.CASCADE,
                                             verbose_name='CatalogoProducto', null=False, blank=False)

    def __str__(self):
        return '{cantidad} de {producto}'.format(cantidad=str(self.cantidad), producto=self.fk_catalogo_producto.fk_producto.nombre)


@python_2_unicode_compatible
class Canasta(models.Model):
    fk_semana = models.ForeignKey(Semana, on_delete=models.CASCADE, verbose_name='Semana', null=False, blank=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    imagen = models.ImageField(upload_to='canastas', verbose_name='Imagne', null=False, blank=False)
    esta_publicada = models.BooleanField(default=False, verbose_name='¿Se encuentra publicada?', null=False, blank=False)

    def __str__(self):
        return self.nombre

    @property
    def productos(self):
        return CanastaProducto.objects.filter(fk_canasta_id=self.id)

    @property
    def get_precio(self):
        return '{0:.2f}'.format(self.precio)

    @property
    def precio(self):
        precio = Decimal('0')
        for producto in self.productos:
            precio += Decimal(str(producto.fk_producto_catalogo.precio)) * producto.cantidad
        return precio

    @property
    def get_estado(self):
        return 'Publicada' if self.esta_publicada else 'Sin publicar'

    class Meta:
        verbose_name = 'Canasta'
        verbose_name_plural = 'Canastas'


@python_2_unicode_compatible
class CanastaProducto(models.Model):
    fk_canasta = models.ForeignKey(Canasta, on_delete=models.CASCADE, verbose_name='Canasta', null=False, blank=False)
    fk_producto_catalogo = models.ForeignKey(Catalogo_Producto, on_delete=models.CASCADE, verbose_name='Producto', null=False, blank=False)
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad', null=False, blank=False)

    @property
    def nombre_producto(self):
        return self.fk_producto_catalogo.fk_producto.nombre

    @property
    def precio_producto(self):
        return self.fk_producto_catalogo.precio

    @property
    def unidad_producto(self):
        return self.fk_producto_catalogo.fk_producto.unidad_medida


    @property
    def imagen_producto(self):
        imagen = self.fk_producto_catalogo.fk_producto.imagen
        return imagen.url if imagen else ''

    class Meta:
        verbose_name = 'Producto de canasta'
        verbose_name_plural = 'Productos de canastas'
        unique_together = (('fk_canasta', 'fk_producto_catalogo'),)

    def __str__(self):
        return 'Canasta {canasta} - {producto}'.format(canasta=self.fk_canasta.nombre, producto=self.fk_producto_catalogo.fk_producto)

