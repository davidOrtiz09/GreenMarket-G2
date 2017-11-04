__author__ = 'asistente'
from unittest import TestCase
from selenium import webdriver
import time

def current_milli_time():
    int(round(time.time() * 1000))


class FunctionalTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_detail(self):
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(3)

        nameIndex=self.browser.find_element_by_id('product-name-index')
        descriptionIndex=self.browser.find_element_by_id('product-description-index')
        priceIndex=self.browser.find_element_by_id('product-price-index')

        link = self.browser.find_element_by_id('button-detail')
        link.click()
        self.browser.implicitly_wait(2)

        name = self.browser.find_element_by_id('product-name-test')
        description= self.browser.find_element_by_id('description-test')
        price= self.browser.find_element_by_id('product-price-test')

        self.assertEquals(nameIndex.text, name.text)
        self.assertEquals(descriptionIndex.text, description.text)
        self.assertEquals(priceIndex.text, price.text)







