# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from Administrador.models import Pedido
from Administrador.models import Cliente
# Register your models here.
admin.site.register(Pedido)
admin.site.register(Cliente)
