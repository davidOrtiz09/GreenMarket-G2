# -*- coding: utf-8 -*-
from django.contrib.auth.forms import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from MarketPlace.models import Cliente, Pedido


class ClientForm(ModelForm):
    nombre = forms.CharField(max_length=User._meta.get_field('first_name').max_length, label='Nombres')
    apellido = forms.CharField(max_length=User._meta.get_field('last_name').max_length, label='Apellidos')
    departamento = forms.ChoiceField(choices=Cliente._meta.get_field('departamento').choices, label='Departamento')
    ciudad = forms.ChoiceField(choices=Cliente._meta.get_field('ciudad').choices, label='Ciudad')
    numero_identificacion = forms.CharField(max_length=20)
    tipo_identificacion = forms.ChoiceField(choices=Cliente._meta.get_field('tipo_identificacion').choices)
    telefono_contacto = forms.CharField(max_length=15, label='Telefono de Contacto')
    correo = forms.EmailField(max_length=50, label='Correo electrónico')
    direccion = forms.CharField(max_length=150, label='Direcció de Residencia')
    contrasena = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    contrasena2 = forms.CharField(widget=forms.PasswordInput(), label='Confirma tu contraseña')

    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'departamento', 'ciudad', 'numero_identificacion', 'tipo_identificacion', 'telefono_contacto', 'correo', 'direccion', 'contrasena', 'contrasena2']

    def clean_contrasena2(self):
        password = self.cleaned_data['contrasena']
        password2 = self.cleaned_data['contrasena2']
        if password != password2:
            raise forms.ValidationError('Las claves no coinciden.')
        return password2

    def clean_correo(self):
        email = self.cleaned_data['correo']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual registrado.')
        return email


class PaymentForm(ModelForm):
    nombre = forms.CharField(max_length=150, label='Nombre')
    email = forms.EmailField(max_length=50, label='Correo electrónico')
    direccion = forms.CharField(max_length=150, label='Direcció de Residencia')
    celular = forms.CharField(max_length=15, label='Celular')
    telefono = forms.CharField(max_length=15, label='Telefono')
    observaciones = forms.CharField(max_length=500, label='Observaciones')
    nombre_completo = forms.CharField(max_length=150, label='Nombre')
    tipo_documento= forms.ChoiceField(choices=Pedido._meta.get_field('tipo_identificacion').choices)
    numero_documento=forms.CharField(max_length=20)

    class Meta:
         model = Pedido
         fields = ['nombre', 'email', 'direccion', 'celular', 'telefono', 'observaciones', 'nombre_completo','tipo_documento','numero_documento']
    #
    # def clean_correo(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email):
    #         raise forms.ValidationError('Ya existe un email igual registrado.')
    #     return email
