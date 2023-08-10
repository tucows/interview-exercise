import requests


class QuoteAPIClient:
    def __init__(self, base_url="http://api.forismatic.com/api/1.0/"):
        self.base_url = base_url
        self.default_params = {
            "method": "getQuote",
            "format": "json",
            "lang": "en",
            "key": "working",
        }

    def get_random_quote(self, key=None):
        key = key or self.default_params["key"]
        quote_data = {"quote": "No quote available", "author": "", "key": key}
        try:
            params = self.default_params.copy()
            params["key"] = key

            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                quote_data = response.json()

            return {
                "quote": quote_data.get("quoteText", "No quote available"),
                "author": quote_data.get("quoteAuthor", ""),
                "key": key,
            }
        except Exception:
            # returns default message in case of error
            return quote_data
