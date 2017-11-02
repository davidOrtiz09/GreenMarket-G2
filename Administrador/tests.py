# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from GreenMarket.wsgi import application
from django.test import TestCase
from GreenMarket.settings import BASE_DIR
from selenium import webdriver
from MarketPlace.models import Canasta, Catalogo_Producto, CanastaProducto, Catalogo, Producto, Categoria, Cooperativa
from MarketPlace.utils import get_or_create_week
import os
import platform
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta


class AgregarProductoCanasataTest(TestCase):
    def setUp(self):
        cooperativa = Cooperativa.objects.create(
            nombre='Cooperativa',
            ciudad='Ciudad',
            departamento='Departamento'
        )
        cooperativa.save()
        semana = get_or_create_week()
        categoria = Categoria(
            nombre='Nombre de la categoría',
            descripcion='Descripción de la categoría de pruebas',
            imagen='categorias/imagen-pruebas.jpg'
        )
        categoria.save()

        counter = 1
        limit = 10
        while counter <= limit:
            Producto(
                fk_categoria_id=categoria.id,
                nombre='Producto de pruebas {0}'.format(counter),
                descripcion='Descripción del producto de pruebas {0}'.format(counter),
                imagen='productos/producto-prueba-{0}.png'.format(counter),
                fecha_creacion=timezone.now(),
                unidad_medida='Kg'
            ).save()
            counter += 1

        catalogo = Catalogo(
            fk_semana_id=semana.id,
            fecha_creacion=timezone.now(),
            fecha_cierre=timezone.now() + timedelta(days=5)
        )
        catalogo.save()

        productos = Producto.objects.all()
        for producto in productos:
            Catalogo_Producto(
                fk_catalogo=catalogo,
                fk_producto=producto,
                precio=Decimal('1600')
            ).save()

        canasta = Canasta(
            nombre='Canasta de pruebas',
            imagen='canastas/canasta-uvas.jpg',
            precio=Decimal('20000'),
            fk_semana_id=semana.id
        )
        canasta.save()

        if platform.system() == 'Darwin':
            self.browser = webdriver.Chrome(os.path.join(BASE_DIR, 'Administrador', 'chromedriver', 'chromedriver'))
        else:
            self.browser = webdriver.Chrome(os.path.join(BASE_DIR, 'Administrador', 'chromedriver', 'chromedriver.exe'))
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def do_login(self):
        username_str = 'tdduser'
        password_str = 'grupo2agiles'
        self.browser.get('http://127.0.0.1:8000/administrador/ingresar')

        username = self.browser.find_element_by_id('login-username')
        username.send_keys(username_str)

        password = self.browser.find_element_by_id('login-password')
        password.send_keys(password_str)

        boton_login = self.browser.find_element_by_id('login')
        boton_login.click()
        self.browser.implicitly_wait(3)

    def test_login(self):
        self.do_login()
        self.assertIn('Administrador - Green Market', self.browser.title)

    def test_contar_productos_disponibles(self):
        self.do_login()
        primer_canasta = Canasta.objects.first()

        self.browser.get('http://127.0.0.1:8000/administrador/canastas/{id_canasta}'.format(id_canasta=primer_canasta.id))

        divs_productos_disponibles = self.browser.find_elements_by_class_name('producto-disponible')

        ids_productos_canasta = CanastaProducto.objects.filter(
            fk_canasta_id=primer_canasta.id,
        ).values_list('fk_producto_catalogo_id', flat=True)

        productos_disponibles = Catalogo_Producto.objects.filter(
            fk_catalogo__fk_semana_id=primer_canasta.fk_semana_id,
        ).exclude(
            fk_producto_id__in=ids_productos_canasta
        ).distinct()

        self.assertEquals(len(divs_productos_disponibles), productos_disponibles.count())
