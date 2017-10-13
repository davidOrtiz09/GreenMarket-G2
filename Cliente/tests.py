# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from Cliente.models import Cliente


class ClienteTestCase(TestCase):
    def setUp(self):
        django_user_1 = User.objects.create_user(
                username='davideduardo.ortiz@gmail.com',
                password='david123',
                first_name='david',
                last_name='ortiz',
                email='davideduardo.ortiz@gmail.com'
            )
        Cliente.objects.create(fk_django_user=django_user_1, ciudad='1',
                                    departamento='1', telefono_contacto='6966308',
                                    direccion='calle false 123', numero_identificacion='1072664899',
                                    tipo_identificacion='cc')

    def test_clientes_lookup(self):
        django_user = User.objects.get(email='davideduardo.ortiz@gmail.com')
        cliente = Cliente.objects.get(numero_identificacion='1072664899')
        self.assertEqual(cliente.fk_django_user, django_user)
