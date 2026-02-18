from app.services.http_fetcher import fetch_via_http
from app.services.browser_fetcher import fetch_via_browser
from app.services.content_validator import is_valid_content

async def fetch_url(url: str) -> str:
    try:
        content = await fetch_via_http(url)
        if is_valid_content(content):
            return content

        content = await fetch_via_browser(url)
        if is_valid_content(content):
            return content

        raise ValueError("Content invalid after browser fallback.")

    except Exception:
        try:
            content = await fetch_via_browser(url)
            if is_valid_content(content):
                return content
            raise ValueError("Both HTTP and Browser fetch failed.")
        except Exception:
            raise ValueError("Failed to fetch valid content.")
