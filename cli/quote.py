import click
import base64

from services.picture_api import PictureAPIClient
from services.quote_api import QuoteAPIClient


@click.command()
@click.option('--category', default='working', help='Category key for the API.')
@click.option('--grayscale/--no-grayscale', default=False, help='Retrieve a grayscale image.')
@click.option('--output-quote', default='quote.txt', help='Output file for the quote.')
@click.option('--output-image', default='image.jpg', help='Output file for the image.')
def main(category, grayscale, output_quote, output_image):
    try:
        # Create API clients
        picture_api_client = PictureAPIClient()
        quote_api_client = QuoteAPIClient()

        # Get random quote
        quote_data = quote_api_client.get_random_quote(category)
        quote_text = quote_data['quote']
        quote_author = quote_data['author']

        # Get random image
        image_data_base64 = picture_api_client.get_random_picture(grayscale=grayscale)

        # Save quote to file
        with open(output_quote, 'w') as quote_file:
            quote_file.write(f'Quote: {quote_text}\nAuthor: {quote_author}\n')

        # Save image to file
        image_content = base64.b64decode(image_data_base64)
        with open(output_image, 'wb') as image_file:
            image_file.write(image_content)

        print(f'Quote saved to: {output_quote}')
        print(f'Image saved to: {output_image}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
