from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from fastapi.responses import JSONResponse

# Import custom modules for fetching the latest news and summarizing content
from news_fetcher import get_latest_news
from summarizer import summarize_text

# Create an instance of FastAPI for building the web API
app = FastAPI()

# Setup Jinja2 for rendering templates (e.g., HTML files stored in the 'templates' directory)
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JavaScript, or images) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route for rendering the home page, served using an HTML template (index.html)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # The 'request' object is passed to the template for rendering dynamic content
    return templates.TemplateResponse("index.html", {"request": request})

# Route for fetching news articles and summarizing them
@app.get("/news")
def fetch_and_summarize_news(category: str = Query(None), query: str = Query(None)):
    try:
        # Fetch the latest news articles based on the optional 'category' and 'query' parameters
        articles = get_latest_news(category, query)
        
        # If no articles are found, return an empty list in the JSON response
        if not articles:
            return JSONResponse(content={"news": []}, status_code=200)
        
        # Create a list of summarized articles by extracting the title and summarizing the content
        summarized_articles = [
            {
                "title": article["title"], 
                "description": article.get("description", "No Description"), 
                "summary": summarize_text(article["content"]),
                "thumbnail": article.get("thumbnail"),
                "url": article.get("url", "#")
            }  # Summarize the content of the article
            for article in articles if "title" in article and "content" in article  # Ensure article has both title and content fields
        ]

        # Return the summarized articles as a JSON response with a 200 status code (OK)
        return JSONResponse(content={"news": summarized_articles}, status_code=200)

    except Exception as e:
        # If an error occurs during the fetching or summarizing process, log the error and return an internal server error response
        print(f"Error: {str(e)}")  # Logs the error message to the terminal for debugging purposes
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)
