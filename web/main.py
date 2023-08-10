from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from services.picture_api import PictureAPIClient
from services.quote_api import QuoteAPIClient

app = FastAPI()

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Depends

# Create an instance of Jinja2Templates
templates = Jinja2Templates(directory="./web/static")
app.mount("/web/static", StaticFiles(directory="web/static"), name="static")


# Create instances of the API client classes as dependable so it can be injected into the app
def get_quote_service():
    return QuoteAPIClient()


def get_picture_service():
    return PictureAPIClient()


@app.get("/", response_class=HTMLResponse)
def get_random_quote_and_picture(
    request: Request,
    key: str = None,
    grayscale: bool = False,
    quote_client=Depends(get_quote_service),
    picture_client=Depends(get_picture_service),
):
    quote_response = quote_client.get_random_quote(key=key)
    picture_content = picture_client.get_random_picture(grayscale=grayscale)

    # Render the HTML template
    template_data = {
        "IMAGE_BASE64": picture_content,
        "QUOTE_TEXT": quote_response["quote"],
        "QUOTE_AUTHOR": quote_response["author"],
        "CATEGORY": quote_response["key"],
        "INPUT_CHECKED": "checked" if grayscale else "",
    }

    return templates.TemplateResponse(
        "index.html", {"request": request, **template_data}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
