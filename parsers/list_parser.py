from bs4 import BeautifulSoup


def _parse_card(item) -> dict:
    title_tag = item.select_one(".thumb a img")
    link_tag = item.select_one(".thumb a")
    thumb_tag = item.select_one(".thumb a img")
    eps_tag = item.select_one(".thumb .epz")
    genre_tags = item.select(".set .genres a")
    rating_tag = item.select_one(".set .rating i")

    title = title_tag.get("alt", "").strip() if title_tag else ""
    link = link_tag.get("href", "") if link_tag else ""
    thumb = thumb_tag.get("src", "") if thumb_tag else ""
    episode = eps_tag.get_text(strip=True) if eps_tag else ""
    genres = [g.get_text(strip=True) for g in genre_tags]
    rating = rating_tag.get_text(strip=True) if rating_tag else ""
    slug = link.rstrip("/").split("/")[-1] if link else ""

    return {
        "title": title,
        "slug": slug,
        "url": link,
        "thumb": thumb,
        "episode": episode,
        "genres": genres,
        "rating": rating,
    }


def parse_anime_list(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    items = []
    for card in soup.select(".venz ul li"):
        items.append(_parse_card(card))

    # Pagination
    pagination = {}
    prev_page = soup.select_one(".pagination .prev a")
    next_page = soup.select_one(".pagination .next a")
    pagination["prev"] = prev_page.get("href", "") if prev_page else None
    pagination["next"] = next_page.get("href", "") if next_page else None

    return {"anime": items, "pagination": pagination}
