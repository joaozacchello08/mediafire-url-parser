from fastapi import FastAPI
from requests import get
from bs4 import BeautifulSoup as bs

app = FastAPI()

@app.get("/")
def root():
    return { "message": "Hello World!" }

@app.get("/api/{mediafire_url:path}")
def get_url(mediafire_url: str):
    if "https://www.mediafire.com" not in mediafire_url:
        return { "message": "Invalid URL." }, 400
    
    try:
        resp = get(mediafire_url)
        data = bs(resp.text, "html.parser")
        element = data.find("a", attrs={ "id": "downloadButton" })

        if not element:
            raise AttributeError("Couldn't parse mediafire URL.")
        
        result_url = element.get("href")
        return { "message": "URL was parsed successfully!", "result": result_url }, 200
    except Exception as e:
        return { "message": f"An error occurred trying to parse mediafire URL: {str(e)}" }, 500
