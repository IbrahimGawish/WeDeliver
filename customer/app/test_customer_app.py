import unittest
from flask import Flask
from app import customers_data

class CustomerAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

    def tearDown(self):
        pass

    def test_invoices_data(self):
        with self.app.app_context():
            result = customers_data()
            self.assertIsInstance(result, list)

    def test_index_route(self):
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('Customers Data', data)

    def test_hello_route(self):
        with self.app.test_client() as client:
            response = client.get('/api/sayHello')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_data(as_text=True), "Hello, Welcome to Customer Service")

if __name__ == '__main__':
    unittest.main()
