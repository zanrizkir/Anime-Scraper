from bs4 import BeautifulSoup


def _parse_card(item) -> dict:
    # Title from .jdlflm (most reliable in card layout)
    title_tag = item.select_one(".jdlflm")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Fallback: try img alt
    if not title:
        img_alt = item.select_one(".thumb img")
        title = img_alt.get("alt", "").strip() if img_alt else ""

    # Link & slug
    link_tag = item.select_one(".thumb a")
    link = link_tag.get("href", "") if link_tag else ""
    slug = link.rstrip("/").split("/")[-1] if link else ""

    # Thumbnail image
    thumb_tag = item.select_one(".thumb img")
    thumb = thumb_tag.get("src", "") if thumb_tag else ""

    # Episode count — .epz is inside .detpost, not .thumb
    eps_tag = item.select_one(".epz")
    episode = eps_tag.get_text(strip=True) if eps_tag else ""

    # Day or rating from .epztipe
    epztipe_tag = item.select_one(".epztipe")
    sub_info = epztipe_tag.get_text(strip=True) if epztipe_tag else ""

    # Date from .newnime
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


def parse_anime_list(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    items = []
    for card in soup.select(".venz ul li"):
        items.append(_parse_card(card))

    # Pagination — uses .pagenavix with a.next / a.prev
    pagination = {}
    prev_page = soup.select_one(".pagenavix a.prev")
    next_page = soup.select_one(".pagenavix a.next")
    pagination["prev"] = prev_page.get("href", "") if prev_page else None
    pagination["next"] = next_page.get("href", "") if next_page else None

    return {"anime": items, "pagination": pagination}
