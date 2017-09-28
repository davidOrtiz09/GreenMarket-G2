# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
# -*-
from django import forms

class Cliente(models.Model):
    TIPO_DOCUMENTOS = (
        ('CC', 'Cédula de Ciudadanía'),
        ('PA', 'Pasaporte'),
        ('CE', 'Cédula de Extranjería'),
        ('RC', 'Registro Civil')
    )

    ##TODO: Cargar ciudades y departamentos

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=False, null=False, blank=False)
    apellido = models.CharField(max_length=150, unique=False, null=False, blank=False)
    departamento = models.CharField(max_length=20, unique=False, null=False, blank=False)
    ciudad = models.CharField(max_length=20, unique=False, null=False, blank=False)
    numero_identificacion = models.CharField(max_length=20)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_DOCUMENTOS)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El nùmero debe tener el formato correcto")
    telefono_contacto = models.CharField(validators=[phone_regex], max_length=15, null=False, blank=False)
    correo = models.EmailField(max_length=20)
    direccion = models.CharField(max_length=150, null=False, blank=False)
    contrasena = models.CharField(widget=forms.PasswordInput)

    class Meta:
        unique_together = ('numero_identificacion', 'tipo_identificacion',)
