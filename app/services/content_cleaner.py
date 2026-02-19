import re
import trafilatura
from bs4 import BeautifulSoup

def extract_main_content(html: str) -> str:
    """
    Extract meaningful main text from HTML.
    Removes scripts, styles, navbars, and layout noise.
    """

    # Try trafilatura first (best for article extraction)
    extracted = trafilatura.extract(html)
    if extracted:
        return normalize_text(extracted)

    # Fallback: BeautifulSoup cleanup
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    return normalize_text(text)


def normalize_text(text: str) -> str:
    """
    Normalize text to reduce meaningless diffs.
    """
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    text = re.sub(r"\d{1,2}:\d{2}", "", text)  # remove timestamps like 12:45
    text = re.sub(r"\b\d+\b", "", text)  # remove isolated numbers (vote counts etc.)
    return text.strip()
