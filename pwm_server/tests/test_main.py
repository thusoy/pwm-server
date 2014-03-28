from pwm_server import create_app

from os import path
import unittest

class MainPageTest(unittest.TestCase):

    def setUp(self):
        test_config = path.abspath(path.join(path.dirname(__file__), 'config.py'))
        self.app = create_app(test_config)
        self.client = self.app.test_client()


    def test_main(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
