__author__ = 'asistente'
from unittest import TestCase
from selenium import webdriver
import time

def current_milli_time():
    int(round(time.time() * 1000))


class FunctionalTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('C:\\Users\\Diego\\Downloads\\chromedriver_win32\\chromedriver.exe')
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_detail(self):
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

    def do_login(self):
        username_str = 'test@test.com'
        password_str = '123456789'
        self.browser.get('http://127.0.0.1:8000/')

        loginB = self.browser.find_element_by_id('login-ingresar')
        loginB.click()

        time.sleep(2)
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

    def test_cart(self):
        self.do_login()
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(5)

        time.sleep(2)
        self.browser.get('http://localhost:8000#product-image-index-1')
        link = self.browser.find_element_by_id('product-image-index-1')
        link.click()
        self.browser.implicitly_wait(5)

        link_plus = self.browser.find_element_by_id('plusAgregarProductoPopUp-1')
        link_plus.click()
        link_plus.click()
        link_plus.click()

        link_min = self.browser.find_element_by_id('minusAgregarProductoPopUp-1')
        link_min.click()
        link_min.click()

        self.browser.implicitly_wait(2)

        quantity = self.browser.find_element_by_id('agregarProductoPopUp-1')
        quantity.click()

        alter_m = self.browser.find_element_by_class_name('alert')

        self.assertEquals('Por favor ingresa a tu cuenta para agregar items a tu carrito', alter_m.text)