import unittest
from unittest.mock import patch, MagicMock
from app import app, vehicles_data
class TestVehicleApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('your_flask_app.mysql.connector.connect')
    @patch('your_flask_app.mysql.connector.Cursor')
    def test_vehicles_data(self, mock_cursor, mock_connect):
        # Mocking the database connection and cursor
        connection_mock = MagicMock()
        cursor_mock = MagicMock()

        # Set up the mock results you expect from the database query
        mock_results = [{'id': 1, 'vehicle_type': 'Car', 'vehicle_status': 'Leased',
                         'rent_price': 10, 'onboard_date': '2023-12-28 12:00:00'},
                        {'id': 2, 'vehicle_type': 'Motorcycle', 'vehicle_status': 'Leased',
                         'rent_price': 5, 'onboard_date': '2023-12-20 12:00:00'}]

        cursor_mock.fetchall.return_value = mock_results
        mock_cursor.return_value = cursor_mock
        mock_connect.return_value = connection_mock

        # Make the request to the vehicles_data route
        response = self.app.get('/')
        data = response.get_json()

        # Assert the response contains the expected data
        self.assertEqual(response.status_code, 200)
        self.assertIn('Vehicles Data', data)
        self.assertEqual(data['Vehicles Data'], mock_results)

    def test_hello_route(self):
        response = self.app.get('/api/sayHello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, Welcome to Vehicle Service')

if __name__ == '__main__':
    unittest.main()
