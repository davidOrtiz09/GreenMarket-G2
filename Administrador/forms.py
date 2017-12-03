from django.contrib.auth.forms import forms
from django.forms import ModelForm

from MarketPlace.models import Cooperativa


class CooperativaForm(ModelForm):
    nombre = forms.CharField(max_length=Cooperativa._meta.get_field('nombre').max_length, label='Nombre')
    departamento = forms.CharField(max_length=Cooperativa._meta.get_field('departamento').max_length, label='Departamento')
    ciudad = forms.CharField(max_length=Cooperativa._meta.get_field('ciudad').max_length, label='Ciudad')
    coordenadas_gps = forms.CharField(max_length=Cooperativa._meta.get_field('coordenadas_gps').max_length, label='Coordenadas')

    class Meta:
        model = Cooperativa
        fields = ['nombre', 'departamento', 'ciudad', 'coordenadas_gps']
