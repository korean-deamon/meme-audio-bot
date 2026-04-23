import httpx
from bs4 import BeautifulSoup
import urllib.parse
import logging
import re

logger = logging.getLogger(__name__)

async def search_myinstants(query: str, page: int = 1):
    """
    Search MyInstants with pagination support.
    """
    if not query:
        # Trending page with pagination
        url = f"https://www.myinstants.com/en/index/us/?page={page}"
    else:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.myinstants.com/en/search/?name={encoded_query}&page={page}"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            instants = soup.find_all('div', class_='instant')
            
            results = []
            for i, instant in enumerate(instants):
                try:
                    button = instant.find('button', class_='small-button')
                    if not button:
                        continue
                    
                    onclick = button.get('onclick', '')
                    audio_path = ""
                    if 'play(' in onclick:
                        match = re.search(r"play\('([^']+)'", onclick)
                        if match:
                            audio_path = match.group(1)
                    
                    if not audio_path:
                        continue

                    link_tag = instant.find('a', class_='instant-link')
                    title = link_tag.get_text(strip=True) if link_tag else f"Meme {i+1}"
                    
                    results.append({
                        "id": f"web_{page}_{i}_{hash(audio_path)}",
                        "title": title,
                        "audio_url": f"https://www.myinstants.com{audio_path}"
                    })
                except Exception:
                    continue
            
            return results
    except Exception as e:
        logger.error(f"Scraper error: {e}")
        return []
