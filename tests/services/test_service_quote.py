import unittest
import requests
from unittest.mock import patch
from services.quote_api import QuoteAPIClient


class TestQuoteAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = QuoteAPIClient()

    @patch("requests.get")
    def test_get_random_quote_success(self, mock_get):
        # Set up the mock response
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = (
            b'{"quoteText": "Mock Quote", "quoteAuthor": "Mock Author"}'
        )
        mock_get.return_value = mock_response

        result = self.client.get_random_quote()

        self.assertEqual(result["quote"], "Mock Quote")
        self.assertEqual(result["author"], "Mock Author")

    @patch("requests.get")
    def test_get_random_quote_failure(self, mock_get):
        # Set up the mock response
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.client.get_random_quote()

        self.assertEqual(result["quote"], "No quote available")
        self.assertEqual(result["author"], "")
