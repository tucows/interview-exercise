import os
from click.testing import CliRunner
from unittest.mock import Mock, patch
from cli.quote import main
import base64


# Mock the requests module to simulate API responses
@patch("cli.quote.PictureAPIClient.get_random_picture")
@patch("cli.quote.QuoteAPIClient.get_random_quote")
def test_main_successful(get_random_quote, get_random_picture):
    # Mock the API responses for both quote and image
    get_random_quote.return_value = {
        "quote": "This is a test quote",
        "author": "Test Author",
    }
    image_content = b"fake_picture_content"
    get_random_picture.return_value = base64.b64encode(image_content)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--category",
            "test-category",
            "--grayscale",
            "--output-quote",
            "test_quote.txt",
            "--output-image",
            "test_image.jpg",
        ],
    )

    assert result.exit_code == 0
    assert (
        result.output.strip()
        == "Quote saved to: test_quote.txt\nImage saved to: test_image.jpg"
    )

    # Check if the output files exist and contain the expected content
    assert os.path.isfile("test_quote.txt")
    assert os.path.isfile("test_image.jpg")
    with open("test_quote.txt", "r") as quote_file:
        message = quote_file.read().strip()
        assert message == "Quote: This is a test quote\nAuthor: Test Author"
    with open("test_image.jpg", "rb") as image_file:
        assert image_file.read() == image_content

    # Clean up
    os.remove("test_quote.txt")
    os.remove("test_image.jpg")


@patch("cli.quote.PictureAPIClient.get_random_picture")
@patch("cli.quote.QuoteAPIClient.get_random_quote")
def test_main_no_grayscale(get_random_quote, get_random_picture):
    # Mock the API responses for both quote and image
    get_random_quote.return_value = {
        "quote": "This is a test quote",
        "author": "Test Author",
    }
    image_content = b"fake_picture_content"
    get_random_picture.return_value = base64.b64encode(image_content)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--category",
            "test-category",
            "--output-quote",
            "test_quote.txt",
            "--output-image",
            "test_image.jpg",
        ],
    )

    assert result.exit_code == 0
    assert (
        result.output.strip()
        == "Quote saved to: test_quote.txt\nImage saved to: test_image.jpg"
    )

    # Clean up
    os.remove("test_quote.txt")
    os.remove("test_image.jpg")


@patch("cli.quote.PictureAPIClient.get_random_picture")
@patch("cli.quote.QuoteAPIClient.get_random_quote")
def test_main_no_outputs(get_random_quote, get_random_picture):
    # Mock the API responses for both quote and image
    get_random_quote.return_value = {
        "quote": "This is a test quote",
        "author": "Test Author",
    }
    image_content = b"fake_picture_content"
    get_random_picture.return_value = base64.b64encode(image_content)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--category",
            "test-category",
            "--grayscale",
        ],
    )

    assert result.exit_code == 0
    assert (
        result.output.strip() == "Quote saved to: quote.txt\nImage saved to: image.jpg"
    )

    # Check if the output files exist and contain the expected content
    assert os.path.isfile("quote.txt")
    assert os.path.isfile("image.jpg")
    with open("quote.txt", "r") as quote_file:
        message = quote_file.read().strip()
        assert message == "Quote: This is a test quote\nAuthor: Test Author"
    with open("image.jpg", "rb") as image_file:
        assert image_file.read() == image_content

    # Clean up
    os.remove("quote.txt")
    os.remove("image.jpg")


@patch("cli.quote.PictureAPIClient.get_default_image")
@patch("services.picture_api.requests.get")
@patch("services.quote_api.requests.get")
def test_main_api_error(get_random_quote, get_random_picture, get_default_image):
    # Mock the API responses for both quote and image with errors
    get_random_quote.side_effect = Exception("mocked error")
    get_random_picture.side_effect = Exception("mocked error")
    fake_picture_content = b"fake_picture_content"
    get_default_image.return_value = base64.b64encode(fake_picture_content)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--category",
            "test-category",
            "--grayscale",
            "--output-quote",
            "test_quote.txt",
            "--output-image",
            "test_image.jpg",
        ],
    )

    assert result.exit_code == 0
    assert (
        result.output.strip()
        == "Quote saved to: test_quote.txt\nImage saved to: test_image.jpg"
    )

    # Check if the default quote ("No quote available") is saved to the output file
    assert os.path.isfile("test_quote.txt")
    with open("test_quote.txt", "r") as quote_file:
        assert quote_file.read().strip() == "Quote: No quote available\nAuthor:"

    # Check if the default image is saved to the output file
    assert os.path.isfile("test_image.jpg")
    with open("test_image.jpg", "rb") as image_file:
        assert image_file.read() == fake_picture_content

    # Clean up
    os.remove("test_quote.txt")
    os.remove("test_image.jpg")
