import unittest
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen

from run import app


class StylingAndStatusCode(LiveServerTestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8824
        return app

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.close()

    def test_index_returns_200_code(self):
        response = urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_layout_and_styling(self):
        self.driver.get(self.get_server_url())
        self.driver.set_window_size(1024, 768)
        # And there is an element for the EUR currency
        # which contains a red dot within the sparkline
        eur_sparkline = self.driver.find_element_by_id('circleEUR')
        self.assertEqual(eur_sparkline.value_of_css_property('fill'),
            'rgb(255, 0, 0)')

if __name__ == "__main__":
    unittest.main()