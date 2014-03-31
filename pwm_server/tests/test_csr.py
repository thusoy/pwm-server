from pwm_server import create_app, db
from pwm_server.models import Certificate

from os import path
import textwrap
import unittest

class MainPageTest(unittest.TestCase):

    def setUp(self):
        test_config = path.abspath(path.join(path.dirname(__file__), 'config.py'))
        self.app = create_app(test_config)
        self.app.bootstrap()
        self.client = self.app.test_client()


    def test_new_csr(self):
        csr = open(path.join(path.dirname(__file__), 'data', 'test.csr')).read()
        files = {'content': csr}
        response = self.client.post('/ca/csr', data=files)
        self.assertEqual(response.status_code, 202)
        with self.app.app_context():
            certs = Certificate.query.all()
            self.assertEqual(1, len(certs))


    def test_invalid_new_csr(self):
        # No csr sent
        response = self.client.post('/ca/csr')
        self.assertEqual(response.status_code, 400)

        # Invalid csr contents
        response = self.client.post('/ca/csr', data={'content': 'foobar'})
        self.assertEqual(response.status_code, 400)

        # Invalid csr contents
        content = textwrap.dedent("""\
                     -----BEGIN CERTIFICATE REQUEST-----
                     yumyum
                     -----END CERTIFICATE REQUEST-----""")
        response = self.client.post('/ca/csr', data={'content': content})
        self.assertEqual(response.status_code, 400)



