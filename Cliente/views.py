# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from Cliente.forms import ClientForm
from Cliente.models import Cliente


class Index(View):
    def get(self, request):
        return render(request, 'Cliente/index.html', {})


def add_client_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre = cleaned_data.get('nombre')
            apellido = cleaned_data.get('apellido')
            contrasena = cleaned_data.get('contrasena')
            ciudad = cleaned_data.get('ciudad')
            departamento = cleaned_data.get('departamento')
            telefono_contacto = cleaned_data.get('telefono_contacto')
            correo = cleaned_data.get('correo')
            direccion = cleaned_data.get('direccion')
            numero_identificacion = cleaned_data.get('numero_identificacion')
            tipo_identificacion = cleaned_data.get('tipo_identificacion')

            cliente_model = Cliente(nombre=nombre, appellido=apellido,
                                    contrasena=contrasena, ciudad=ciudad,
                                    departamento=departamento,telefono_contacto=telefono_contacto,
                                    correo=correo, direccion=direccion, numero_identificacion=numero_identificacion,
                                    tipo_identificacion=tipo_identificacion
                                    )
            cliente_model.save()
    else:
        form = ClientForm()
        return render(request, 'Cliente/registrar_cliente.html', {'form': form})


