import unittest
from unittest.mock import patch
from services.picture_api import PictureAPIClient
import base64


class TestPictureAPIClient(unittest.TestCase):
    @patch("services.picture_api.requests.get")
    def test_get_random_picture(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_picture_content"
        mock_get.return_value = mock_response

        api_client = PictureAPIClient()
        result = api_client.get_random_picture()

        self.assertEqual(
            result, "ZmFrZV9waWN0dXJlX2NvbnRlbnQ="
        )  # Base64 encoding of "fake_picture_content"

    @patch("services.picture_api.requests.get")
    def test_get_random_picture_failure(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api_client = PictureAPIClient(static_folder="web/static")
        result = api_client.get_random_picture()

        self.assertEqual(result, api_client.get_default_image())

    def test_get_default_image(self):
        api_client = PictureAPIClient(static_folder="web/static")
        result = api_client.get_default_image()

        with open("web/static/unavailable.png", "rb") as image_file:
            expected_data = image_file.read()
            expected_base64 = base64.b64encode(expected_data).decode("utf-8")

        self.assertEqual(result, expected_base64)
