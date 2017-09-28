# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# -*-
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombres', unique=False, null=False, blank=False)
    apellido = models.CharField(max_length=150, verbose_name='Apellidos', unique=False, null=False, blank=False)
    departamento = models.CharField(max_length=20, verbose_name='Departamento', unique=False, null=False, blank=False)
    ciudad = models.CharField(max_length=20, verbose_name='Ciudad', unique=False, null=False, blank=False)
    numero_identificacion = models.CharField(max_length=20, verbose_name='Numero Identificacion', unique=True, null=False, blank=False)
    tipo_identificacion = models.CharField(max_length=2, verbose_name='Tipo Identificacion', null=False, blank=False)
    telefono_contacto = models.CharField(max_length=20, verbose_name='Telefono Contacto', null=False, blank=False)
    correo = models.CharField(max_length=20, verbose_name='Correo', null=False, blank=False)
    direccion = models.CharField(max_length=150, verbose_name='Direccion', null=False, blank=False)
    contrasena = models.CharField(max_length=10, verbose_name='Contrasena', null=False, blank=False)
