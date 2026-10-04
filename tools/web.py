import re
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MultiAgentBookWriter/1.0)"}

def search_web(query: str, max_results: int = 8) -> list[dict]:
  url = "https://html.duckduckgo.com/html/?q=" + quote(query)
  r = requests.get(url, headers=HEADERS, timeout=20)
  r.raise_for_status()
  soup = BeautifulSoup(r.text, "html.parser")
  results = []
  for a in soup.select("a.result__a")[:max_results]:
    href = a.get("href", "")
    title = a.get_text(" ", strip=True)
    if href.startswith("http"):
      results.append({"title": title, "url": href})
  return results

def fetch_page(url: str, timeout: int = 20) -> dict:
  r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
  r.raise_for_status()
  soup = BeautifulSoup(r.text, "html.parser")
  for tag in soup(["script", "style", "noscript"]):
    tag.decompose()
  text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
  return {"url": r.url, "title": soup.title.get_text(strip=True) if soup.title else r.url, "text": text}

def fetch_url(url: str, timeout: int = 20) -> tuple[bool, str]:
  try:
    return True, fetch_page(url, timeout)["text"]
  except Exception as exc:
    return False, str(exc)
