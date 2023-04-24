"""The module contains test suites for white box unit testing of the API."""

from unittest.mock import patch
import requests.exceptions
from django.test import TestCase
from rest_framework.test import APITestCase
import api.views as views
from api.views import LIST_OF_CODES


class APIRouteTest(APITestCase):
    """The class verifies the correctness of the application's API calls."""

    def test_available_codes_pass(self):
        response = self.client.get('/api/v1/codes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"codes": LIST_OF_CODES})

    @patch('api.views.fetch_data', return_value={
        'rates': [
            {'ask': 4.0, 'bid': 3.9},
            {'ask': 4.1, 'bid': 4.0},
            {'ask': 4.2, 'bid': 3.8},
        ]
    })
    def test_biggest_diff_pass(self, mock_fetch_data):
        response = self.client.get('/api/v1/diff/usd/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'major difference': 0.4})

    @patch('api.views.fetch_data', return_value={
        'rates': [
            {'mid': 4.0},
            {'mid': 4.1},
            {'mid': 4.2},
        ]
    })
    def test_minimax_per_period_pass(self, mock_fetch_data):
        response = self.client.get('/api/v1/minimax/usd/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"minimum average value": 4.0,
                                           "maximum average value": 4.2})

    @patch('api.views.fetch_data', return_value={
        'rates': [
            {'mid': 4.0},
        ]
    })
    def test_rate_per_day_pass(self, mock_fetch_data):
        response = self.client.get('/api/v1/average/usd/2023-03-01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"average rate": 4.0})

    def test_rate_per_day_fail(self):
        response = self.client.get('/api/v1/average/usd/2023-04-16/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Error": "Unfortunately, "
                                                    "NBP does not provide the data for weekends or holidays."})


class FunctionsTest(TestCase):
    """The class verifies the correctness of the data processing
    and validation functions of API app.
    """

    def test_validate_period_pass(self):
        self.assertTrue(views.validate_period(255))
        self.assertTrue(views.validate_period(1))

    def test_validate_period_fail(self):
        self.assertFalse(views.validate_period(256))
        self.assertFalse(views.validate_period(0))
        self.assertFalse(views.validate_period(-1))

    def test_validate_date_pass(self):
        self.assertTrue(views.validate_date('2023-04-23'))

    def test_validate_date_fail(self):
        self.assertFalse(views.validate_date('2222222'))

    @patch('api.views.list_of_codes', return_values=['usd', 'eur'])
    def test_validate_code_pass(self, mock_list_of_codes):
        self.assertTrue(views.validate_code('usd', mock_list_of_codes))

    @patch('api.views.list_of_codes', return_values=['usd', 'eur'])
    def test_validate_code_not_in_list_fail(self, mock_list_of_codes):
        self.assertFalse(views.validate_code('zzz', mock_list_of_codes))

    @patch('api.views.list_of_codes', return_value=[])
    def test_validate_code_list_is_none_fail(self, mock_list_of_codes):
        self.assertFalse(views.validate_code('usd', mock_list_of_codes.return_value))

    def test_list_of_codes_pass(self):
        codes = views.list_of_codes()
        self.assertIn('USD', codes)

    def test_list_of_codes_non_empty_list_pass(self):
        codes = views.list_of_codes()
        self.assertTrue(codes)

    @patch('api.views.requests.get', side_effect=requests.exceptions.Timeout)
    def test_list_of_codes_timeout(self, mock_get):
        codes = views.list_of_codes()
        self.assertEqual(codes, [])

    def test_fetch_data_pass(self):
        data = views.fetch_data('http://api.nbp.pl/api/exchangerates/rates/a/usd/last/3/')
        self.assertIsNotNone(data)

    @patch('api.views.requests.get', side_effect=requests.exceptions.Timeout)
    def test_fetch_data_timeout(self, mock_get):
        data = views.fetch_data('https://example.com/api')
        self.assertIsNone(data)
