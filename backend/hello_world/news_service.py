import requests
import os
from dotenv import load_dotenv

load_dotenv()

# NewsData.io API Key
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsdata.io/api/1/latest"

def fetch_news(category=None, query=None, size=5, country="in", language="en"):
    """
    Fetches news with rich metadata for professional UI display.
    """
    params = {
        'apikey': API_KEY,
        'size': size,
        'country': country,
        'language': language,
        'image': 1,              # Ensure we get articles with images
        'removeduplicate': 1
    }

    if query:
        params['q'] = query
    if category:
        params['category'] = category

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = data.get('results', [])
        formatted_news = []

        for art in articles:
            # We clean up the creator field since it's often a list or None
            creators = art.get("creator")
            author = ", ".join(creators) if isinstance(creators, list) else (creators or "Staff Writer")

            formatted_news.append({
                "title": art.get("title", "Breaking News"),
                "description": art.get("description", "No description available for this story."),
                "link": art.get("link", "#"),
                "image": art.get("image_url", ""),
                "source_name": art.get("source_name", "Global News"),
                "source_icon": art.get("source_icon", ""), # Useful for a small favicon in UI
                "author": author,
                "published_at": art.get("pubDate", "Recently"),
                "source_id": art.get("source_id", "news")
            })
            
        return formatted_news

    except Exception as e:
        print(f"NewsData.io Fetch Error: {e}")
        return []

# --- Quick Local Test ---
if __name__ == "__main__":
    print("Testing Rich Data Fetch (Tech)...")
    results = fetch_news(category="politics", size=1)
    if results:
        print(f"TITLE: {results[0]['title']}")
        print(f"SOURCE: {results[0]['source_name']} (Icon: {results[0]['source_icon']})")
        print(f"AUTHOR: {results[0]['author']}")
        print(f"DATE: {results[0]['published_at']}")