import unittest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from web.main import app, get_quote_service, get_picture_service


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_quote_client = Mock()
        self.mock_picture_client = Mock()
        app.dependency_overrides[get_quote_service] = lambda: self.mock_quote_client
        app.dependency_overrides[get_picture_service] = lambda: self.mock_picture_client

    def tearDown(self):
        app.dependency_overrides = {}

    def test_get_random_quote_and_picture(self):
        self.mock_quote_client.get_random_quote.return_value = {
            "quote": "Test quote",
            "author": "Test author",
            "key": "test_category",
        }
        self.mock_picture_client.get_random_picture.return_value = "test_base64_image"

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test quote", response.content)
        self.assertIn(b"Test author", response.content)
        self.assertIn(b"test_category", response.content)
        self.assertIn(
            b"checked", response.content
        )  # Check if grayscale checkbox is checked

    def test_get_random_quote_and_picture_with_grayscale(self):
        self.mock_quote_client.get_random_quote.return_value = {
            "quote": "Test quote",
            "author": "Test author",
            "key": "test_category",
        }
        self.mock_picture_client.get_random_picture.return_value = "test_base64_image"

        response = self.client.get("/?grayscale=True")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test quote", response.content)
        self.assertIn(b"Test author", response.content)
        self.assertIn(b"test_category", response.content)
        self.assertIn(
            b"checked", response.content
        )  # Check if grayscale checkbox is checked


if __name__ == "__main__":
    unittest.main()
