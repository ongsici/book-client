from fastapi import FastAPI, Query
import requests  
import os
from dotenv import load_dotenv
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles


load_dotenv()

BOOK_DATA_URL = os.getenv("BOOK_DATA_URL")
BOOK_DATA_PORT = os.getenv("BOOK_DATA_PORT")
BOOK_DATA_ENDPOINT = os.getenv("BOOK_DATA_ENDPOINT")

BOOK_DATA_API = f"http://{BOOK_DATA_URL}:{BOOK_DATA_PORT}/{BOOK_DATA_ENDPOINT}"
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    message = "Use the dropdown to select a genre and/or type a book title to search for books."
    return templates.TemplateResponse("index.html", {"request": request, "message": message})


@app.get("/get_books", response_class=HTMLResponse)
async def get_books(request: Request,  genre: str = Query(None), title: str = Query(None)):
    try:
        response = requests.get(BOOK_DATA_API)
        response.raise_for_status() 
        if response.status_code == 200:
            books = response.json()
            if genre:
                filtered_books = [book for book in books if genre.lower() in book['genre'].lower()]
            if title:
                filtered_books = [book for book in filtered_books if title.lower() in book['title'].lower()]
            if not genre and not title:
                filtered_books = books  

            return templates.TemplateResponse("results.html", {"request": request, "filtered_books": filtered_books})

    except requests.RequestException as e:
        return {"error": f"An error occurred while requesting data: {e}"}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
