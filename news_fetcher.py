import requests
from config import NEWS_API_KEY  # Import the API key from the config file

# Default image URL when no thumbnail is provided
DEFAULT_THUMBNAIL_URL = "/static/images/mega.jpg"

# Function to fetch the latest news based on optional category and query parameters
def get_latest_news(category=None, query=None):
    # Base URL for the News API
    base_url = "https://newsapi.org/v2/top-headlines"
    
    # Parameters to send in the API request
    params = {"country": "us", "apiKey": NEWS_API_KEY}  # 'us' country and the API key for authentication

    # Add category to parameters if provided
    if category:
        params["category"] = category

    # Add search query to parameters if provided
    if query:
        params["q"] = query

    try:
        # Make the API request with the specified parameters
        response = requests.get(base_url, params=params)
        
        # Raise an exception for non-200 responses
        response.raise_for_status()

        # Parse the JSON response
        news_data = response.json()
        
        # Extract articles
        articles = news_data.get("articles", [])

        # Return an empty list if no articles found
        if not articles:
            return []

        # ✅ Include default thumbnail if 'urlToImage' is unavailable
        return [
            {
                "title": article.get("title", "No Title"),
                "description": article.get("description", "No Description"),  # ✅ Add description
                "content": article.get("content", "No Content"),
                "thumbnail": article.get("urlToImage", DEFAULT_THUMBNAIL_URL),  # ✅ Add default image
                "url": article.get("url", "#")  # ✅ Add URL field
            }
            for article in articles if article
        ]

    except requests.exceptions.RequestException as e:
        print(f"News API Error: {str(e)}")  # Log errors for debugging
        return []
