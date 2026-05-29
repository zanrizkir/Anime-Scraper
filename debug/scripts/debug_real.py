"""Debug: fetch home page, get actual anime URLs, then try accessing one."""
import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

HTML_DIR = os.path.join(PROJECT_ROOT, "debug", "html")

from utils.browser import fetch_html
from config import BASE_URL
from bs4 import BeautifulSoup


async def main():
    # 1. Get real anime links from home page (which works)
    print("=== Fetching home page ===")
    html = await fetch_html(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")
    
    # Find actual anime detail links
    anime_links = []
    for item in soup.select(".venz ul li"):
        link_tag = item.select_one(".thumb a")
        if link_tag:
            href = link_tag.get("href", "")
            title_tag = item.select_one("img")
            title = title_tag.get("alt", "") if title_tag else ""
            anime_links.append({"title": title, "url": href})
    
    print(f"Found {len(anime_links)} anime links from home page")
    for al in anime_links[:5]:
        print(f"  {al['title'][:50]} -> {al['url']}")
    
    if not anime_links:
        return
    
    # 2. Try to access the first anime detail page using the ACTUAL URL from home
    test_url = anime_links[0]["url"]
    print(f"\n=== Testing anime detail URL: {test_url} ===")
    html2 = await fetch_html(test_url)
    soup2 = BeautifulSoup(html2, "html.parser")
    
    title = soup2.title.get_text(strip=True) if soup2.title else "(no title)"
    print(f"Page title: {title}")
    
    with open(os.path.join(HTML_DIR, "debug_anime_real.html"), "w", encoding="utf-8") as f:
        f.write(html2)
    print(f"Saved debug_anime_real.html ({len(html2)} bytes)")
    
    # Check content
    for sel_name, sel in [
        ("infozingle", ".infozingle"),
        ("infozin", ".infozin"),
        ("spe", ".spe"),
        ("fotoanime", ".fotoanime"),
        ("sinopc", ".sinopc"),
        ("sinops", ".sinops"),
        ("episodelist", "#episodelist"),
        ("entry-title", "h1.entry-title"),
        ("infox", ".infox"),
    ]:
        found = soup2.select(sel)
        if found:
            text = found[0].get_text(strip=True)[:80]
            print(f"  FOUND '{sel_name}': {text}")
    
    # 3. Check if the URL pattern is different (maybe not /anime/ but something else)
    print("\n=== All internal links from the interstitial page ===")
    html3 = await fetch_html(f"{BASE_URL}/anime/youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e-season-4-sub-indo/")
    soup3 = BeautifulSoup(html3, "html.parser")
    
    # Look for safelinks or actual content links
    all_a = soup3.find_all("a")
    for a in all_a:
        href = a.get("href", "")
        text = a.get_text(strip=True)[:40]
        if href and not href.startswith("#") and "facebook" not in href:
            print(f"  [{text}] -> {href}")
    
    # 4. Check if there's JS content that loads via AJAX
    scripts = soup3.find_all("script")
    for s in scripts:
        text = s.get_text()
        if text.strip() and len(text.strip()) > 10:
            print(f"\n  SCRIPT: {text[:300]}")


if __name__ == "__main__":
    asyncio.run(main())
