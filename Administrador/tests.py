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


class AdministradorTests(TestCase):
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

        canasta2 = Canasta(
            nombre='Canasta de pruebas2',
            imagen='canastas/canasta-uvas.jpg',
            precio=Decimal('22000'),
            fk_semana_id=semana.id
        )
        canasta2.save()

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

    def productos_disponibles_canasta(self, canasta):
        ids_productos_canasta = CanastaProducto.objects.filter(
            fk_canasta_id=canasta.id,
        ).values_list('fk_producto_catalogo_id', flat=True)

        productos_disponibles = Catalogo_Producto.objects.filter(
            fk_catalogo__fk_semana_id=canasta.fk_semana_id,
        ).exclude(
            fk_producto_id__in=ids_productos_canasta
        ).distinct()
        return productos_disponibles

    def test_contar_productos_disponibles(self):
        self.do_login()
        canasta = Canasta.objects.last()

        self.browser.get('http://127.0.0.1:8000/administrador/canastas/2')

        divs_productos_disponibles = self.browser.find_elements_by_class_name('producto-disponible')
        productos_disponibles = self.productos_disponibles_canasta(canasta)

        self.assertEquals(len(divs_productos_disponibles), productos_disponibles.count())

    def test_agregar_producto(self):
        self.do_login()
        primer_canasta = Canasta.objects.first()

        self.browser.get(
            'http://127.0.0.1:8000/administrador/canastas/{id_canasta}'.format(id_canasta=primer_canasta.id))

        divs_productos_disponibles = self.browser.find_elements_by_class_name('producto-disponible')
        divs_productos_agregados = self.browser.find_elements_by_class_name('producto-agregado')

        boton = self.browser.find_element_by_class_name('btn-agregar-producto')
        boton.click()
        self.browser.implicitly_wait(5)

        divs_productos_disponibles2 = self.browser.find_elements_by_class_name('producto-disponible')
        divs_productos_agregados2 = self.browser.find_elements_by_class_name('producto-agregado')

        self.assertEqual(len(divs_productos_disponibles), len(divs_productos_disponibles2) + 1)
        self.assertEqual(len(divs_productos_agregados), len(divs_productos_agregados2) - 1)

    def test_lista(self):
        self.do_login()
        self.browser.get('http://127.0.0.1:8000/administrador/informes')
        self.browser.implicitly_wait(3)
        text = self.browser.find_element_by_xpath(
            "//select[@id='tipo_informe']/option[text()='Ver inventarios']")
        self.assertIn('Ver inventarios', text.text)

    def test_ir_informe_inventario(self):
        self.do_login()
        self.browser.get('http://127.0.0.1:8000/administrador/informes')
        self.browser.implicitly_wait(3)
        text = self.browser.find_element_by_xpath(
            "//select[@id='tipo_informe']/option[text()='Ver inventarios']")

        text.click()
        self.browser.implicitly_wait(3)

        th_table = self.browser.find_element_by_xpath(
            "//table/thead/tr/th[text()='Inventario semana']")

        self.assertIn('Inventario semana', th_table.text)

    def test_consultar_campos_tabla(self):
        self.do_login()
        self.browser.get('http://127.0.0.1:8000/administrador/informes')
        self.browser.implicitly_wait(3)
        text = self.browser.find_element_by_xpath(
            "//select[@id='tipo_informe']/option[text()='Ver inventarios']")
        text.click()
        self.browser.implicitly_wait(3)

        tr_th_table = self.browser.find_element_by_xpath(
            "//table/thead/tr/th[text()='Producto']")

        self.assertIn('Producto', tr_th_table.text)

        tr_th_table = self.browser.find_element_by_xpath(
            "//table/thead/tr/th[text()='Total Productos']")

        self.assertIn('Total Productos', tr_th_table.text)

        tr_th_table = self.browser.find_element_by_xpath(
            "//table/thead/tr/th[text()='Cantidad Vendida']")

        self.assertIn('Cantidad Vendida', tr_th_table.text)

        tr_th_table = self.browser.find_element_by_xpath(
            "//table/thead/tr/th[text()='Cantidad Disponible']")

        self.assertIn('Cantidad Disponible', tr_th_table.text)
