# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your tests here.
from django.test import TestCase
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait


class Test(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("C:\\Users\\JUAN CIFUENTES\\chromedriver.exe")
        # self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)


    def tearDown(self):
        self.browser.quit()


    def test_lista(self):
        self.do_login()
        self.browser.get('http://127.0.0.1:8000/administrador/informes')
        self.browser.implicitly_wait(3)
        text=self.browser.find_element_by_xpath(
            "//select[@id='tipo_informe']/option[text()='Ver inventarios']")
        self.assertIn('Ver inventarios', text.text)

    def test_ir_informe_inventario(self):
        self.do_login()
        self.browser.get('http://127.0.0.1:8000/administrador/informes')
        self.browser.implicitly_wait(3)
        text=self.browser.find_element_by_xpath(
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

    def do_login(self):
        username_str = 'jc.cifuentes'
        password_str = 'Maria0517*'
        self.browser.get('http://127.0.0.1:8000/administrador/ingresar')

        username = self.browser.find_element_by_id('login-username')
        username.send_keys(username_str)

        password = self.browser.find_element_by_id('login-password')
        password.send_keys(password_str)

        boton_login = self.browser.find_element_by_id('login')
        boton_login.click()
        self.browser.implicitly_wait(3)