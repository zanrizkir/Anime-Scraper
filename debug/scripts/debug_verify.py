"""Verify all parsers against saved HTML files."""
import sys
import json
import os

# Add project root to path so we can import parsers/utils/config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

HTML_DIR = os.path.join(PROJECT_ROOT, "debug", "html")

sys.stdout.reconfigure(encoding="utf-8")

from parsers.home_parser import parse_home
from parsers.list_parser import parse_anime_list
from parsers.search_parser import parse_search
from parsers.genre_parser import parse_genres, parse_genre_anime
from parsers.schedule_parser import parse_schedule
from parsers.anime_parser import parse_anime_detail


def test(name, filename, parser_fn):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    filepath = os.path.join(HTML_DIR, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        result = parser_fn(html)
        # Pretty print but limit output
        output = json.dumps(result, ensure_ascii=False, indent=2)
        lines = output.split("\n")
        if len(lines) > 40:
            print("\n".join(lines[:40]))
            print(f"  ... ({len(lines) - 40} more lines)")
        else:
            print(output)
        print(f"\n[OK] {name} parsed successfully")
    except Exception as e:
        print(f"[ERR] {name}: {e}")
        import traceback
        traceback.print_exc()


test("Home", "debug_home.html", parse_home)
test("Ongoing", "debug_ongoing.html", parse_anime_list)
test("Search (naruto)", "debug_search.html", parse_search)
test("Genre List", "debug_genres_list.html", parse_genres)
test("Genre Anime (action)", "debug_genres_action.html", parse_genre_anime)
test("Schedule", "debug_schedule.html", parse_schedule)
test("Anime Detail", "debug_anime_real.html", parse_anime_detail)
