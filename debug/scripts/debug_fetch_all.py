"""
Debug script: fetch HTML from multiple otakudesu.blog pages and save to files.
Run this to capture real HTML for parser debugging.
"""
import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

HTML_DIR = os.path.join(PROJECT_ROOT, "debug", "html")

if sys.platform.startswith("win"):
    ver = sys.version_info
    if (ver.major, ver.minor) < (3, 14):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from utils.browser import fetch_html
from config import BASE_URL

PAGES = {
    "debug_home.html": BASE_URL,
    "debug_ongoing.html": f"{BASE_URL}/ongoing-anime/page/1/",
    "debug_completed.html": f"{BASE_URL}/complete-anime/page/1/",
    "debug_search.html": f"{BASE_URL}/?s=naruto&post_type=anime",
    "debug_genres_list.html": f"{BASE_URL}/genre-list/",
    "debug_genres_action.html": f"{BASE_URL}/genres/action/page/1/",
    "debug_schedule.html": f"{BASE_URL}/jadwal-rilis/",
}


async def main():
    os.makedirs(HTML_DIR, exist_ok=True)
    for filename, url in PAGES.items():
        print(f"\n{'='*60}")
        print(f"Fetching: {url}")
        filepath = os.path.join(HTML_DIR, filename)
        print(f"Saving to: {filepath}")
        try:
            html = await fetch_html(url)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[OK] Saved ({len(html)} bytes)")
        except Exception as e:
            print(f"[ERR] Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
