"""Debug script: fetch anime detail, home, episode, search, schedule pages and inspect HTML."""
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


async def debug_anime_detail():
    print("=" * 80)
    print("DEBUGGING: ANIME DETAIL PAGE")
    print("=" * 80)
    url = f"{BASE_URL}/anime/youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e-season-4-sub-indo/"
    print(f"Fetching: {url}")
    html = await fetch_html(url)

    with open(os.path.join(HTML_DIR, "debug_anime.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved HTML ({len(html)} bytes)")

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "(no title)"
    print(f"Page title: {title}")

    # 1. Synopsis
    print("\n--- Synopsis selectors ---")
    for sel in [".sinopc", ".sinops", ".entry-content .synops", ".synops", "#sinopsis", ".spe + div", ".entry-content p"]:
        found = soup.select(sel)
        if found:
            text = found[0].get_text(strip=True)[:100]
            print(f"  '{sel}': {len(found)} items -> {text}...")

    # 2. Info / metadata
    print("\n--- Info selectors ---")
    for sel in [".infozingle p", ".infozin p", ".infozingle span", ".spe span", ".info-content span", ".infox .spe span"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items")
            for f_item in found[:3]:
                print(f"    -> {f_item.get_text(strip=True)[:80]}")

    # 3. Genre links inside info
    print("\n--- Genre link selectors ---")
    for sel in [".infozingle .genres-anime a", ".infozin a", ".spe a", ".infox a", ".genxed a", ".infozingle a"]:
        found = soup.select(sel)
        if found:
            texts = [f.get_text(strip=True) for f in found[:5]]
            print(f"  '{sel}': {len(found)} items -> {texts}")

    # 4. Episode list
    print("\n--- Episode list selectors ---")
    for sel in ["#episodelist li", ".episodelist li", "#episodelist ul li", ".eplister li", ".episodelist ul li"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items")
            for f_item in found[:3]:
                a = f_item.select_one("a")
                if a:
                    print(f"    -> {a.get_text(strip=True)[:60]} | {a.get('href','')}")

    # 5. Batch link
    print("\n--- Batch link selectors ---")
    for sel in [".batchlink a", ".batch a", ".dlbod a", "#batch a", ".vemark a"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items -> {found[0].get('href','')}")

    # 6. Thumb
    print("\n--- Thumb selectors ---")
    for sel in [".fotoanime img", ".thumb img", ".thumbook img", ".infoanime img", ".animeinfo img"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items -> {found[0].get('src','')[:80]}")

    # 7. Title
    print("\n--- Title selectors ---")
    for sel in ["h1.entry-title", ".entry-title", ".jdlrx h1", "h1"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items -> {found[0].get_text(strip=True)[:80]}")

    # 8. Deep inspect info structure
    print("\n--- Deep inspect: all <span> inside .spe or .infozingle ---")
    for span in soup.select(".spe span, .infozingle span")[:15]:
        full = span.decode_contents()[:120]
        text = span.get_text(separator="|", strip=True)[:100]
        print(f"  HTML: {full}")
        print(f"  Text: {text}")
        print()


async def debug_home():
    print("\n" + "=" * 80)
    print("DEBUGGING: HOME PAGE")
    print("=" * 80)
    html = await fetch_html(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")

    print("\n--- Home section selectors ---")
    for sel in ["#recent-release", "#new-anime", ".vemark", ".rseries", ".rapi", ".venz"]:
        found = soup.select(sel)
        if found:
            children = found[0].select("li")
            print(f"  '{sel}': found, {len(children)} <li> children")

    # Alternative ongoing/completed
    for sel in [".venz ul li"]:
        found = soup.select(sel)
        if found:
            print(f"\n  '{sel}': {len(found)} items")
            for item in found[:2]:
                title_tag = item.select_one("img")
                title = title_tag.get("alt", "") if title_tag else "(no img)"
                print(f"    -> {title[:60]}")

    # Check .detpost, .thumb
    print("\n--- Card structure ---")
    for sel in [".detpost", ".thumb", ".thumbz", ".rseries .rapi"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items")


async def debug_schedule():
    print("\n" + "=" * 80)
    print("DEBUGGING: SCHEDULE PAGE")
    print("=" * 80)
    url = f"{BASE_URL}/jadwal-rilis/"
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    for sel in [".kglist321", ".schedulepage", "#jadwal"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items")
            for block in found[:2]:
                h2 = block.select_one("h2")
                lis = block.select("li")
                print(f"    day={h2.get_text(strip=True) if h2 else '?'}, items={len(lis)}")


async def debug_search():
    print("\n" + "=" * 80)
    print("DEBUGGING: SEARCH PAGE")
    print("=" * 80)
    url = f"{BASE_URL}/?s=naruto&post_type=anime"
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    for sel in [".chivsrc ul li", ".chivsrc li", ".column-content li", "#venkonten li"]:
        found = soup.select(sel)
        if found:
            print(f"  '{sel}': {len(found)} items")
            for item in found[:2]:
                a = item.select_one("a")
                print(f"    -> {a.get_text(strip=True)[:60] if a else '(no link)'}")


async def main():
    await debug_anime_detail()
    await debug_home()
    await debug_schedule()
    await debug_search()


if __name__ == "__main__":
    asyncio.run(main())
