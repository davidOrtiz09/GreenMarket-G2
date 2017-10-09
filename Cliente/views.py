# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.views import View
from Cliente.forms import ClientForm
from Cliente.models import Cliente
from django.contrib.auth.models import User


class Index(View):
    def get(self, request):
        return render(request, 'Cliente/index.html', {})


def add_client_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
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

            user_model = User.objects.create_user(
                username=correo,
                password=contrasena,
                first_name=nombre,
                last_name=apellido,
                email=correo
            )
            user_model.save()
            cliente_model = Cliente(fk_django_user=user_model, ciudad=ciudad,
                                    departamento=departamento, telefono_contacto=telefono_contacto,
                                    direccion=direccion, numero_identificacion=numero_identificacion,
                                    tipo_identificacion=tipo_identificacion
                                    )
            cliente_model.save()
            return render(request, 'Cliente/index.html', {})
        else:
            context = {
                'form': form
            }
            return render_to_response('Cliente/registrar_cliente.html', context)
    else:
        form = ClientForm()
        context = {
            'form': form
        }
        return render(request, 'Cliente/registrar_cliente.html', context)
