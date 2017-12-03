# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from GreenMarket.wsgi import application
from selenium import webdriver
import time
from MarketPlace.models import Canasta, Catalogo_Producto, CanastaProducto, Catalogo, Producto, Categoria, Cooperativa
from MarketPlace.utils import get_or_create_week
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import platform
import os
from GreenMarket.settings import BASE_DIR


# Create your tests here.
from MarketPlace.models import Cliente


class ClienteTestCase(TestCase):
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

        if platform.system() == 'Darwin':
            self.browser = webdriver.Chrome(os.path.join(BASE_DIR, 'Administrador', 'chromedriver', 'chromedriver'))
        elif platform.system() == 'Linux':
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.Chrome(os.path.join(BASE_DIR, 'Administrador', 'chromedriver', 'chromedriver.exe'))

        self.browser.implicitly_wait(2000000000)

    def do_login(self):
        username_str = 'qwerty@gmail.com'
        password_str = 'qwerty123'
        self.browser.get('http://127.0.0.1:8000/')

        loginB = self.browser.find_element_by_id('login-ingresar')
        loginB.click()

        username = self.browser.find_element_by_id('login-username')
        username.send_keys(username_str)

        password = self.browser.find_element_by_id('login-password')
        password.send_keys(password_str)

        boton_login = self.browser.find_element_by_id('login')
        boton_login.click()
        usuario_actual = self.browser.find_element_by_id('usuario-actual')
        self.browser.implicitly_wait(3)
        self.assertFalse(usuario_actual.text=="" )

    def test_login(self):
        self.do_login()
        usuario_actual = self.browser.find_element_by_id('usuario-actual')
        self.assertFalse(usuario_actual.text == "")

    def tearDown(self):
        self.browser.quit()

    def test_detail(self):
        self.do_login()
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(3)

        time.sleep(2)
        self.browser.get('http://localhost:8000#product-image-index-1')
        nameIndex=self.browser.find_element_by_id('product-name-index-1')
        time.sleep(2)
        priceIndex=self.browser.find_element_by_id('product-price-index-1')

        time.sleep(2)
        link = self.browser.find_element_by_id('product-image-index-1')
        time.sleep(2)
        link.click()

        name = self.browser.find_element_by_id('product-name-popup-1')
        price= self.browser.find_element_by_id('product-price-popup-1')

        self.assertEquals(nameIndex.text, name.text)
        self.assertEquals(priceIndex.text, price.text)

    def test_cart(self):
        self.do_login()
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(5)

        link = self.browser.find_element_by_id('button-detail')
        link.click()
        self.browser.implicitly_wait(5)

        link_plus = self.browser.find_element_by_id('add-quantity-plus')
        link_plus.click()
        link_plus.click()
        link_plus.click()

        link_min = self.browser.find_element_by_id('add-quantity-min')
        link_min.click()

        link_min = self.browser.find_element_by_id('add-quantity-min')
        link_min.click()
        self.browser.implicitly_wait(2)

        quantity = self.browser.find_element_by_id('add-quantity-cart')
        quantity.click()

        alter_m = self.browser.find_element_by_class_name('alert')

        self.assertEquals('Por favor ingresa a tu cuenta para agregar items a tu carrito', alter_m.text)