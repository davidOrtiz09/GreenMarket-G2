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







