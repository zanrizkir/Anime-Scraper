from bs4 import BeautifulSoup


def _parse_home_card(item) -> dict:
    """Parse a single anime card from the homepage .venz section."""
    # Title from .jdlflm (most reliable)
    title_tag = item.select_one(".jdlflm")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Fallback: try img alt
    if not title:
        img_tag = item.select_one(".thumb img")
        title = img_tag.get("alt", "").strip() if img_tag else ""

    # Link & slug
    link_tag = item.select_one(".thumb a")
    link = link_tag.get("href", "") if link_tag else ""
    slug = link.rstrip("/").split("/")[-1] if link else ""

    # Thumbnail
    thumb_tag = item.select_one(".thumb img")
    thumb = thumb_tag.get("src", "") if thumb_tag else ""

    # Episode count (e.g. "Episode 9")
    eps_tag = item.select_one(".epz")
    episode = eps_tag.get_text(strip=True) if eps_tag else ""

    # Day or rating (ongoing = day name, completed = score)
    epztipe_tag = item.select_one(".epztipe")
    sub_info = epztipe_tag.get_text(strip=True) if epztipe_tag else ""

    # Date
    date_tag = item.select_one(".newnime")
    date = date_tag.get_text(strip=True) if date_tag else ""

    return {
        "title": title,
        "slug": slug,
        "url": link,
        "thumb": thumb,
        "episode": episode,
        "sub_info": sub_info,
        "date": date,
    }


def parse_home(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    venz_sections = soup.select(".venz")

    # --- Ongoing (first .venz section) ---
    ongoing = []
    if len(venz_sections) > 0:
        for item in venz_sections[0].select("ul li"):
            ongoing.append(_parse_home_card(item))

    # --- Completed (second .venz section) ---
    completed = []
    if len(venz_sections) > 1:
        for item in venz_sections[1].select("ul li"):
            completed.append(_parse_home_card(item))

    return {"ongoing": ongoing, "completed": completed}
