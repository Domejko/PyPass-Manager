import unittest
from unittest.mock import patch
from requests.models import Response

from src.pass_checker import (
    request_api_data,
    get_passwords_leak_count,
    pwned_api_check,
    run_program,
)


class TestPwnedPasswordChecker(unittest.TestCase):

    @patch("requests.get")
    def test_request_api_data(self, mock_get):
        mock_response = Response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        query_char = "ABCDEF"
        response = request_api_data(query_char)

        self.assertEqual(response.status_code, 200)

    def test_get_passwords_leak_count(self):
        fake_response = Response()
        fake_response._content = b"FF2CB655CE08DB53D721D10DC1EBE159D1E:3"
        hash_to_check = "FF2CB655CE08DB53D721D10DC1EBE159D1E"
        count = get_passwords_leak_count(fake_response, hash_to_check)

        self.assertEqual(count, "3")

    @patch("requests.get")
    def test_pwned_api_check(self, mock_get):
        mock_response = Response()
        mock_response._content = b"C6008F9CAB4083784CBD1874F76618D2A97:3"
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        password = "password123"
        count = pwned_api_check(password)

        self.assertEqual(count, "3")
