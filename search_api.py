# search_api.py
import os
from serpapi import GoogleSearch
from tenacity import retry, stop_after_attempt, wait_exponential

# Load SerpAPI key from environment
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Retry decorator: retries 3 times with exponential backoff
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def search_entity(entity, query_template, num_results=3):
    """
    Search for an entity on Google using SerpAPI and return top result snippets.
    
    Args:
        entity (str): The main entity to search for.
        query_template (str): Query template with {entity} placeholder.
        num_results (int): Number of search results to fetch (default 3).

    Returns:
        list: List of dicts containing title, snippet, and link.
    """
    query = query_template.replace("{entity}", entity)
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []
    for r in results.get("organic_results", []):
        snippets.append({
            "title": r.get("title"),
            "snippet": r.get("snippet"),
            "link": r.get("link")
        })

    if not snippets:
        raise ValueError(f"No search results found for '{entity}'")

    return snippets
