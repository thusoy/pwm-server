import os
import requests
import unittest

class CSRTEst(unittest.TestCase):

    def setUp(self):
        self.test_uri = os.environ['PWM_SERVER_TEST_URI']
        self.cert = os.path.join(os.path.dirname(__file__), '..', 'salt', 'ca', 'files', 'certs',
            'root.crt')


    def test_welcome(self):
        response = requests.get(self.test_uri, verify=self.cert)
        self.assertEqual(response.status_code, 200)


    def test_csr(self):
        csr = open(os.path.join(os.path.dirname(__file__), 'test.csr'))
        files = {'csr': csr}
        response = requests.post(self.test_uri + '/ca/csr', verify=self.cert, files=files)
        self.assertEqual(response.status_code, 202)
