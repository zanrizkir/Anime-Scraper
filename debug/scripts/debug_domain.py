"""Debug: test different domains to find where the actual anime detail content lives."""
import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

HTML_DIR = os.path.join(PROJECT_ROOT, "debug", "html")

from utils.browser import fetch_html
from bs4 import BeautifulSoup


async def test_domain(base_url: str, slug: str):
    url = f"{base_url}/anime/{slug}/"
    print(f"\n--- Testing: {url} ---")
    try:
        html = await fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else "(no title)"
        print(f"  Title: {title}")
        
        # Check for actual anime content
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
            ("animeinfo", ".animeinfo"),
            ("anime_info_body", ".anime_info_body"),
        ]:
            found = soup.select(sel)
            if found:
                text = found[0].get_text(strip=True)[:60]
                print(f"  FOUND '{sel_name}': {text}")
        
        # Check for redirect script
        scripts = soup.find_all("script")
        for s in scripts:
            text = s.get_text()
            if "redirect" in text.lower() or "location" in text.lower() or "window.location" in text.lower():
                print(f"  REDIRECT SCRIPT FOUND: {text[:200]}")
        
        # Check meta refresh
        meta_refresh = soup.find("meta", attrs={"http-equiv": "refresh"})
        if meta_refresh:
            print(f"  META REFRESH: {meta_refresh.get('content', '')}")
            
        # Save HTML for inspection
        domain_name = base_url.replace("https://", "").replace("/", "")
        with open(os.path.join(HTML_DIR, f"debug_{domain_name}.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Saved to debug_{domain_name}.html ({len(html)} bytes)")
        
    except Exception as e:
        print(f"  ERROR: {e}")


async def main():
    slug = "youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e-season-4-sub-indo"
    
    domains = [
        "https://otakudesu.blog",
        "https://otakudesu.io",
    ]
    
    for domain in domains:
        await test_domain(domain, slug)


if __name__ == "__main__":
    asyncio.run(main())
