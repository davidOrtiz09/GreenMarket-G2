# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from GreenMarket.wsgi import application
from django.test import TestCase
from GreenMarket.settings import BASE_DIR
from selenium import webdriver
import os


class AgregarProductoCanasataTest(TestCase):
    def setUp(self):
        # self.browser = webdriver.Chrome(os.path.join(BASE_DIR, 'Administrador', 'chromedriver', 'chromedriver'))
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
