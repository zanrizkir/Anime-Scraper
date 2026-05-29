"""Analyze fetched HTML files to determine correct CSS selectors."""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

HTML_DIR = os.path.join(PROJECT_ROOT, "debug", "html")

from bs4 import BeautifulSoup


def analyze_home():
    print("=" * 60)
    print("HOME PAGE ANALYSIS")
    print("=" * 60)
    with open(os.path.join(HTML_DIR, "debug_home.html"), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Check existing selectors
    print(f"#recent-release: {bool(soup.select_one('#recent-release'))}")
    print(f"#new-anime: {bool(soup.select_one('#new-anime'))}")

    # Find all section-like divs
    for div in soup.select("div[class]"):
        cls = " ".join(div.get("class", []))
        keywords = ["rapi", "venz", "rseries", "detpost", "ongoing", "complete",
                     "recent", "new", "rilis", "anime"]
        if any(k in cls.lower() for k in keywords):
            children = len(div.select("li"))
            if children > 0:
                print(f"  class=\"{cls}\" -> {children} li items")

    # Find h2/h3 headings
    for h in soup.select("h2, h3"):
        text = h.get_text(strip=True)
        if text and len(text) < 80:
            parent = h.parent
            parent_cls = " ".join(parent.get("class", [])) if parent and parent.get("class") else "none"
            print(f"  Heading: \"{text}\" -> parent class=\"{parent_cls}\"")

    # Check .venz structure
    for i, venz in enumerate(soup.select(".venz")):
        lis = venz.select("ul li")
        print(f"  .venz[{i}]: {len(lis)} li items")
        if lis:
            first = lis[0]
            # Check inner structure
            thumb = first.select_one(".thumb")
            detpost = first.select_one(".detpost")
            print(f"    .thumb: {bool(thumb)}, .detpost: {bool(detpost)}")
            if thumb:
                a = thumb.select_one("a")
                img = thumb.select_one("img")
                epz = thumb.select_one(".epz")
                epztipe = thumb.select_one(".epztipe")
                nonton = thumb.select_one(".nonton")
                print(f"    a: {bool(a)}, img: {bool(img)}, .epz: {bool(epz)}, .epztipe: {bool(epztipe)}, .nonton: {bool(nonton)}")
                if a:
                    print(f"    href: {a.get('href', '')[:60]}")
                if img:
                    print(f"    alt: {img.get('alt', '')[:60]}")
            if detpost:
                title_tag = detpost.select_one(".jdlflm")
                eps_tag = detpost.select_one(".epz")
                print(f"    .jdlflm: {title_tag.get_text(strip=True)[:50] if title_tag else 'N/A'}")
                print(f"    .epz: {eps_tag.get_text(strip=True) if eps_tag else 'N/A'}")
                # Show all child classes
                for child in detpost.select("[class]"):
                    child_cls = " ".join(child.get("class", []))
                    child_text = child.get_text(strip=True)[:40]
                    print(f"    detpost child: class=\"{child_cls}\" text=\"{child_text}\"")


def analyze_ongoing():
    print("\n" + "=" * 60)
    print("ONGOING PAGE ANALYSIS")
    print("=" * 60)
    with open(os.path.join(HTML_DIR, "debug_ongoing.html"), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Check current selector
    cards = soup.select(".venz ul li")
    print(f".venz ul li: {len(cards)} items")

    if cards:
        card = cards[0]
        print("\nFirst card structure:")
        # Check all selectors
        tests = {
            ".thumb a img[alt]": card.select_one(".thumb a img"),
            ".thumb a[href]": card.select_one(".thumb a"),
            ".thumb .epz": card.select_one(".thumb .epz"),
            ".thumb .epztipe": card.select_one(".thumb .epztipe"),
            ".set .genres a": card.select(".set .genres a"),
            ".set .rating i": card.select_one(".set .rating i"),
            ".detpost": card.select_one(".detpost"),
            ".detpost .jdlflm": card.select_one(".detpost .jdlflm"),
        }
        for sel, result in tests.items():
            if isinstance(result, list):
                print(f"  {sel}: {len(result)} items -> {[r.get_text(strip=True) for r in result[:3]]}")
            elif result:
                text = result.get_text(strip=True)[:50] if result else ""
                print(f"  {sel}: found -> \"{text}\"")
            else:
                print(f"  {sel}: NOT FOUND")

        # Show raw child structure
        print("\n  All child classes in first card:")
        for child in card.select("[class]"):
            child_cls = " ".join(child.get("class", []))
            child_text = child.get_text(strip=True)[:60]
            print(f"    class=\"{child_cls}\" -> \"{child_text}\"")

    # Pagination
    prev_p = soup.select_one(".pagination .prev a")
    next_p = soup.select_one(".pagination .next a")
    print(f"\n.pagination .prev a: {bool(prev_p)}")
    print(f".pagination .next a: {bool(next_p)}")

    # Alternative pagination selectors
    for sel in [".pagenavix", ".page-nav", "a.next", "a.prev", ".hpage"]:
        result = soup.select(sel)
        if result:
            print(f"  {sel}: {len(result)} -> {[r.get_text(strip=True)[:30] for r in result[:3]]}")


def analyze_search():
    print("\n" + "=" * 60)
    print("SEARCH PAGE ANALYSIS")
    print("=" * 60)
    with open(os.path.join(HTML_DIR, "debug_search.html"), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Check current selector
    print(f".chivsrc ul li: {len(soup.select('.chivsrc ul li'))}")
    print(f".chivsrc li: {len(soup.select('.chivsrc li'))}")
    print(f".chivsrc: {bool(soup.select_one('.chivsrc'))}")

    # Try alternative search selectors
    for sel in [".page ul li", "ul.chivsrc li", ".chivsrc > li", "li", ".col-anime"]:
        items = soup.select(sel)
        if items and len(items) < 100:
            print(f"  {sel}: {len(items)} items")

    # Find the search results container
    for div in soup.select("div[class], ul[class]"):
        cls = " ".join(div.get("class", []))
        if "chiv" in cls.lower() or "search" in cls.lower() or "result" in cls.lower():
            children = len(div.find_all("li", recursive=False))
            a_tags = len(div.select("a"))
            print(f"  class=\"{cls}\" -> {children} direct li, {a_tags} links")
            # Show first child structure
            first_li = div.find("li")
            if first_li:
                print(f"    First li HTML snippet: {str(first_li)[:200]}")


def analyze_genres():
    print("\n" + "=" * 60)
    print("GENRE LIST PAGE ANALYSIS")
    print("=" * 60)
    with open(os.path.join(HTML_DIR, "debug_genres_list.html"), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Check current selector
    genres = soup.select("ul.genres a")
    print(f"ul.genres a: {len(genres)} items")
    if genres:
        print(f"  First 3: {[g.get_text(strip=True) for g in genres[:3]]}")

    # Try alternatives
    for sel in [".genlist a", ".genre-list a", ".genres a", "a[href*='genres']"]:
        items = soup.select(sel)
        if items:
            print(f"  {sel}: {len(items)} items -> {[i.get_text(strip=True) for i in items[:3]]}")


def analyze_genre_anime():
    print("\n" + "=" * 60)
    print("GENRE ANIME PAGE ANALYSIS")
    print("=" * 60)
    with open(os.path.join(HTML_DIR, "debug_genres_action.html"), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    cards = soup.select(".col-anime")
    print(f".col-anime: {len(cards)} items")

    if cards:
        card = cards[0]
        tests = {
            ".col-anime-title a": card.select_one(".col-anime-title a"),
            "img": card.select_one("img"),
            ".col-anime-studio": card.select_one(".col-anime-studio"),
            ".col-anime-rating": card.select_one(".col-anime-rating"),
            ".col-anime-status": card.select_one(".col-anime-status"),
            ".col-anime-eps": card.select_one(".col-anime-eps"),
            ".col-anime-genre": card.select_one(".col-anime-genre"),
            ".col-anime-date": card.select_one(".col-anime-date"),
        }
        for sel, result in tests.items():
            if result:
                print(f"  {sel}: \"{result.get_text(strip=True)[:50]}\"")
            else:
                print(f"  {sel}: NOT FOUND")

        # Show ALL children with classes
        print("\n  Raw card structure:")
        for child in card.select("[class]"):
            child_cls = " ".join(child.get("class", []))
            child_text = child.get_text(strip=True)[:60]
            print(f"    class=\"{child_cls}\" text=\"{child_text}\"")

        # Show raw HTML of first card (limited)
        print(f"\n  First card HTML: {str(card)[:500]}")


def analyze_schedule():
    print("\n" + "=" * 60)
    print("SCHEDULE PAGE ANALYSIS")
    print("=" * 60)
    with open(os.path.join(HTML_DIR, "debug_schedule.html"), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    blocks = soup.select(".kglist321")
    print(f".kglist321: {len(blocks)} blocks")

    if blocks:
        block = blocks[0]
        h2 = block.select_one("h2")
        lis = block.select("li")
        print(f"  h2: \"{h2.get_text(strip=True) if h2 else 'N/A'}\"")
        print(f"  li items: {len(lis)}")
        if lis:
            li = lis[0]
            a = li.select_one("a")
            print(f"  first a href: {a.get('href', '') if a else 'N/A'}")
            print(f"  first a text: {a.get_text(strip=True) if a else 'N/A'}")


def analyze_anime_detail():
    print("\n" + "=" * 60)
    print("ANIME DETAIL PAGE ANALYSIS")
    print("=" * 60)
    with open(os.path.join(HTML_DIR, "debug_anime_real.html"), "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Title
    tests_title = {
        ".infozingle b": soup.select_one(".infozingle b"),
        "h1.entry-title": soup.select_one("h1.entry-title"),
        ".jdlrx h1": soup.select_one(".jdlrx h1"),
        "h1": soup.select_one("h1"),
    }
    for sel, result in tests_title.items():
        print(f"  Title {sel}: \"{result.get_text(strip=True)[:60] if result else 'N/A'}\"")

    # Thumb
    thumb = soup.select_one(".fotoanime img")
    print(f"  .fotoanime img src: {thumb.get('src', '')[:60] if thumb else 'N/A'}")

    # Synopsis
    synopsis = soup.select_one(".sinopc")
    print(f"  .sinopc: {bool(synopsis)}")

    # Info rows
    rows = soup.select(".infozingle p")
    print(f"  .infozingle p: {len(rows)} rows")
    for row in rows[:3]:
        print(f"    -> \"{row.get_text(strip=True)[:80]}\"")

    # Genres
    genre_tests = {
        ".infozingle .genres-anime a": soup.select(".infozingle .genres-anime a"),
        ".infozingle a[rel='tag']": soup.select(".infozingle a[rel='tag']"),
        ".infozingle a": soup.select(".infozingle a"),
    }
    for sel, result in genre_tests.items():
        print(f"  Genres {sel}: {len(result)} -> {[r.get_text(strip=True) for r in result[:5]]}")

    # Episodes
    ep_tests = {
        "#episodelist li": soup.select("#episodelist li"),
        ".episodelist li": soup.select(".episodelist li"),
        ".episodelist ul li": soup.select(".episodelist ul li"),
    }
    for sel, result in ep_tests.items():
        print(f"  Episodes {sel}: {len(result)}")
        if result:
            li = result[0]
            a = li.select_one("a")
            zeebr = li.select_one(".zeebr")
            print(f"    a text: {a.get_text(strip=True)[:60] if a else 'N/A'}")
            print(f"    a href: {a.get('href', '')[:60] if a else 'N/A'}")
            print(f"    .zeebr: {zeebr.get_text(strip=True) if zeebr else 'N/A'}")

    # Batch
    batch_tests = {
        ".batchlink a": soup.select_one(".batchlink a"),
        "a[href*='batch']": soup.select("a[href*='batch']"),
    }
    for sel, result in batch_tests.items():
        if isinstance(result, list):
            print(f"  Batch {sel}: {len(result)} items")
        else:
            print(f"  Batch {sel}: {bool(result)}")


if __name__ == "__main__":
    analyze_home()
    analyze_ongoing()
    analyze_search()
    analyze_genres()
    analyze_genre_anime()
    analyze_schedule()
    analyze_anime_detail()
