import random
import urllib
import base64
import requests


class PictureAPIClient:
    def __init__(self, base_url="https://picsum.photos/", static_folder="static"):
        self.base_url = base_url
        self.static_folder = static_folder

    def get_random_picture(self, width=200, height=300, grayscale=False):
        try:
            picture_params = {"random": random.randint(1, 100)}
            if grayscale:
                picture_params["grayscale"] = ""

            picture_url = f"{self.base_url}{width}/{height}?{urllib.parse.urlencode(picture_params)}"

            response = requests.get(url=picture_url, stream=True)
            if response.status_code == 200:
                picture_content = response.content
                return base64.b64encode(picture_content).decode("utf-8")
            else:
                return self.get_default_image()
        except:
            # Return a default image in case the api can not be accessed
            return self.get_default_image()

    def get_default_image(self):
        with open(f"{self.static_folder}/unavailable.png", "rb") as image_file:
            image_data = image_file.read()
            base64_data = base64.b64encode(image_data).decode("utf-8")
            return base64_data
