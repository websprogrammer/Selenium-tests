# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from time import sleep
import os


class PythonMarketSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('%s\chromedriver' % os.getcwd())
        self.driver.maximize_window()
        self.driver.get('https://yandex.ru')

    def click_to_hidden(self, title):
        element = self.driver.find_element_by_xpath('//*[@class="topmenu__subwrap"]')
        self.driver.execute_script('arguments[0].style.display="block"', element)
        self.driver.find_element_by_xpath('//a[contains(text(), "%s")]' % title).click()
        sleep(2)

    def submit_form(self, inputs, checkboxes, btn):

        for key, value in inputs.items():
            input = self.driver.find_element_by_xpath(key)
            input.send_keys(value)

        for checkbox in checkboxes:
            self.driver.find_element_by_xpath(checkbox).click()

        self.driver.find_element_by_xpath(btn).click()
        sleep(2)

    def make_click(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()
        sleep(2)

    def test_search_in_yandex_market(self):
        driver = self.driver

        self.make_click('//a[@data-id="market"]')
        self.click_to_hidden('Телевизоры')
        self.make_click('//a[contains(text(), "Расширенный поиск")]')

        self.submit_form(
            {'//input[@id="gf-pricefrom-var"]': 20000},
            ('//input[@id="gf-1801946-1871075"]', '//input[@id="gf-1801946-1871447"]'),
            '//button[contains(./span/text(), "Применить")]'
        )

        goods = driver.find_elements_by_xpath('//div[contains(@class, "snippet-card ") and @data-id]//h3')

        if len(goods) == 10:
            first_product = goods[0].text

            self.submit_form(
                {'//input[@id="header-search"]': first_product},
                (),
                '//button[contains(./span/text(), "Найти")]'
            )

            title = driver.find_element_by_xpath('//h1[contains(@class, "title")]').text
            self.assertEqual(first_product, title)

    def test_search_in_yandex_market2(self):
        driver = self.driver

        self.make_click('//a[@data-id="market"]')
        self.click_to_hidden('Плееры')
        self.make_click('//a[text()="Наушники"]')
        self.make_click('//a[contains(text(), "Расширенный поиск")]')

        self.submit_form(
            {'//input[@id="gf-pricefrom-var"]': 5000},
            ('//input[@id="gf-1801946-8455647"]',),
            '//button[contains(./span/text(), "Применить")]'
        )

        goods = driver.find_elements_by_xpath('//div[contains(@class, "snippet-card ") and @data-id]//h3')

        if len(goods) == 10:
            first_product = goods[0].text

            self.submit_form(
                {'//input[@id="header-search"]': first_product},
                (),
                '//button[contains(./span/text(), "Найти")]'
            )

            title = driver.find_element_by_xpath('//h1[contains(@class, "title")]').text
            self.assertEqual(first_product, title)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
