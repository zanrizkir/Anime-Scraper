"""Debug: parse the real anime detail HTML and find correct selectors."""
import sys
import os
import io
import re

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

HTML_DIR = os.path.join(PROJECT_ROOT, "debug", "html")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from bs4 import BeautifulSoup

html = open(os.path.join(HTML_DIR, "debug_anime_real.html"), "r", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")

title = soup.title.get_text(strip=True) if soup.title else "(no title)"
print(f"Page title: {title}")

# Check ALL selectors
sections = {
    "Title": ["h1.entry-title", ".entry-title", ".jdlrx h1", "h1", ".posttl"],
    "Thumb": [".fotoanime img", ".thumb img", ".thumbook img", ".animeinfo img"],
    "Synopsis": [".sinopc", ".sinops", ".entry-content .synops", "#sinopsis", ".desc", ".synops"],
    "Info": [".infozingle p", ".infozin p", ".spe span", ".infox .spe span", ".set span"],
    "Genre": [".infozingle .genres-anime a", ".infozin a", ".infozingle a", ".genxed a", ".genre-info a"],
    "Episodes": ["#episodelist li", ".episodelist li", ".eplister li", ".episodelist ul li"],
    "Batch": [".batchlink a", ".batch a", ".dlbod a"],
}

for section_name, selectors in sections.items():
    print(f"\n{'=' * 60}")
    print(f"  {section_name}")
    print(f"{'=' * 60}")
    for sel in selectors:
        found = soup.select(sel)
        if found:
            print(f"  MATCH '{sel}': {len(found)} items")
            for item in found[:3]:
                text = item.get_text(strip=True)[:100]
                href = item.get("href", "")
                src = item.get("src", "")
                print(f"    text: {text}")
                if href:
                    print(f"    href: {href}")
                if src:
                    print(f"    src: {src}")

# Deep search: find all elements with class containing common keywords
print(f"\n{'=' * 60}")
print(f"  CLASS SEARCH")
print(f"{'=' * 60}")
for el in soup.find_all(class_=re.compile(r'(info|sinop|genre|episo|batch|foto|thumb|spe)', re.I)):
    classes = el.get("class", [])
    tag = el.name
    text = el.get_text(strip=True)[:60]
    print(f"  <{tag} class=\"{' '.join(classes)}\">{text}")

# Also check what's inside the main content area
print(f"\n{'=' * 60}")
print(f"  MAIN CONTENT STRUCTURE (first 3000 chars)")
print(f"{'=' * 60}")
content = soup.select_one("#venkonten") or soup.select_one(".venser") or soup.select_one("#content")
if content:
    # Print structure with indentation
    for child in content.descendants:
        if hasattr(child, 'name') and child.name:
            classes = child.get("class", [])
            cid = child.get("id", "")
            depth = len(list(child.parents))
            desc = f"{'  ' * min(depth, 8)}<{child.name}"
            if cid:
                desc += f' id="{cid}"'
            if classes:
                desc += f' class="{" ".join(classes)}"'
            desc += ">"
            if len(desc) < 120:
                print(desc)
