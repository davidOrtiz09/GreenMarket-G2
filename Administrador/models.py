# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Cliente(models.Model):
    fk_django_user= models.OneToOneField(User, verbose_name='Usuario del sistema', null=False, blank=False)
    tipo_documento = models.CharField(max_length=150, verbose_name='Tipo documento', unique=True, null=False, blank=False)
    documento = models.CharField(max_length=20, verbose_name='Documento', unique=False, null=True, blank=False)
    fecha_nacimiento = models.DateField(verbose_name='Fecha nacemiento', null=False, blank=False)
    direccion = models.CharField(max_length=300, verbose_name='Direccion', null=False, blank=False)

class Pedido(models.Model):
    fk_cliente = models.OneToOneField(Cliente, verbose_name='Cliente', null=False, blank=False)
    fecha_pedido = models.DateField(verbose_name='Fecha del pedido',null=False,blank=False)
    fecha_entrega = models.DateField(verbose_name='Fecha de entrega del pedido', null=False, blank=False)
    estado = models.CharField(max_length=50, verbose_name='Estado', null=False, blank=False)
    valor_total = models.CharField(max_length=300, verbose_name='Valor del pedido', null=False, blank=False)

