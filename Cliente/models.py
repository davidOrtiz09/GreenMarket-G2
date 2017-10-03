# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
# -*-

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

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=False, null=False, blank=False)
    apellido = models.CharField(max_length=150, unique=False, null=False, blank=False)
    departamento = models.CharField(max_length=2, choices=DEPARTAMENTOS)
    ciudad = models.CharField(max_length=2, choices=CIUDADES)
    numero_identificacion = models.CharField(max_length=20)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_DOCUMENTOS)
    telefono_contacto = models.CharField(max_length=15, null=False, blank=False)
    correo = models.EmailField(max_length=20)
    direccion = models.CharField(max_length=150, null=False, blank=False)
    contrasena = models.CharField(max_length=150, null=False, blank=False)

    class Meta:
        unique_together = ('numero_identificacion', 'tipo_identificacion',)
