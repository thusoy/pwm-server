from pwm_server import create_app, db
from pwm_server.models import Certificate

import json
from os import path
from pwm import Domain
import unittest

class MainPageTest(unittest.TestCase):

    def setUp(self):
        test_config = path.abspath(path.join(path.dirname(__file__), 'config.py'))
        self.app = create_app(test_config)
        self.client = self.app.test_client()


    def test_main(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class SaltFetchTest(unittest.TestCase):

    def setUp(self):
        test_config = path.abspath(path.join(path.dirname(__file__), 'config.py'))
        self.app = create_app(test_config)
        self.app.bootstrap()
        self.client = self.app.test_client()
        with self.app.app_context():
            domain = Domain(name='example.com')
            db.session.add(domain)
            db.session.commit()


    def test_search(self):
        response = self.client.get('/domains?q=example')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data)
        self.assertEqual(len(json_response['domains']), 1)
        self.assertTrue(json_response['domains'][0]['name'], 'example.com')


    def test_create_domain(self):
        data = {
            'name': 'facebook.com',
            'alphabet': 'full',
            'length': 16,
        }
        response = self.client.post('/domains', data=data)
        self.assertEqual(response.status_code, 201)
        with self.app.app_context():
            domains = db.session.query(Domain).all()
            self.assertEqual(len(domains), 2)


    def test_create_invalid_domain(self):
        data = {
            'name': 'facebook.com',
            # Must specify alphabet
            # Must specify key length
        }
        response = self.client.post('/domains', data=data)
        self.assertEqual(response.status_code, 400)
