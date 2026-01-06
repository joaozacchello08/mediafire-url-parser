from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from requests import get
from bs4 import BeautifulSoup as bs
import uvicorn

app = FastAPI()
#region html
html = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>MediaFire Parser</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #111;
            color: #eee;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }

        .box {
            background: #1c1c1c;
            padding: 24px;
            border-radius: 8px;
            width: 400px;
            text-align: center;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 12px 0;
            border-radius: 4px;
            border: none;
        }

        button {
            padding: 10px 16px;
            border: none;
            border-radius: 4px;
            background: #4caf50;
            color: #000;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background: #43a047;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>MediaFire Link Parser</h2>
        <input id="url" placeholder="Cole a URL do MediaFire aqui (https://mediafire.com/...)">
        <button onclick="go()">Gerar link</button>
    </div>

    <script>
        function go() {
            const url = document.getElementById("url").value.trim();
            if (!url) return alert("URL vazia.");

            window.location.href = "/api/" + encodeURIComponent(url);
        }
    </script>
</body>
</html>
'''
#endregion

@app.get("/", response_class=HTMLResponse)
def home():
    return html

@app.get("/api/{mediafire_url:path}", response_class=HTMLResponse or JSONResponse)
def get_url(mediafire_url: str):
    if "https://www.mediafire.com" not in mediafire_url:
        return { "message": "Invalid URL." }, 400
    
    try:
        resp = get(mediafire_url)
        data = bs(resp.text, "html.parser")
        element = data.find("a", attrs={ "id": "downloadButton" })

        if not element:
            raise AttributeError("Couldn't parse mediafire URL.")
        
        # if everything ok
        result_url = element.get("href")
        html_content = f'<html><head><title>your mediafire link is ready!</title></head><body><h1><a href="{result_url}">SEU LINK</a></h1></body></html>'
        return html_content
        # return { "message": "URL was parsed successfully!", "result": result_url }, 200
    except Exception as e:
        return { "message": f"An error occurred trying to parse mediafire URL: {str(e)}" }, 500
