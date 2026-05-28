from bs4 import BeautifulSoup


def _parse_anime_card(item) -> dict:
    """Parse a single anime card element."""
    title_tag = item.select_one(".thumb a img")
    link_tag = item.select_one(".thumb a")
    thumb_tag = item.select_one(".thumb a img")
    eps_tag = item.select_one(".thumb .epz") or item.select_one(".thumb .epztipe")
    status_tag = item.select_one(".thumb .epztipe")

    title = title_tag.get("alt", "").strip() if title_tag else ""
    link = link_tag.get("href", "") if link_tag else ""
    thumb = thumb_tag.get("src", "") if thumb_tag else ""
    episode = eps_tag.get_text(strip=True) if eps_tag else ""
    status = status_tag.get_text(strip=True) if status_tag else ""

    # Derive slug from URL  e.g. /anime/naruto/ -> naruto
    slug = link.rstrip("/").split("/")[-1] if link else ""

    return {
        "title": title,
        "slug": slug,
        "url": link,
        "thumb": thumb,
        "episode": episode,
        "status": status,
    }


def parse_home(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # --- Ongoing ---
    ongoing_section = soup.select_one("#recent-release")
    ongoing = []
    if ongoing_section:
        for item in ongoing_section.select("li"):
            ongoing.append(_parse_anime_card(item))

    # --- Completed ---
    completed_section = soup.select_one("#new-anime")
    completed = []
    if completed_section:
        for item in completed_section.select("li"):
            completed.append(_parse_anime_card(item))

    return {"ongoing": ongoing, "completed": completed}
