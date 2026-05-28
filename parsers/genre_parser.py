from bs4 import BeautifulSoup


def parse_genres(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    genres = []
    for a_tag in soup.select(".genres-list a"):
        name = a_tag.get_text(strip=True)
        link = a_tag.get("href", "")
        # URL pattern: /genres/slug/
        slug = link.rstrip("/").split("/")[-1]
        genres.append({"name": name, "slug": slug, "url": link})
    return genres


def parse_genre_anime(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    items = []
    for card in soup.select(".col-anime"):
        title_tag = card.select_one(".col-anime-title a")
        thumb_tag = card.select_one("img")
        studio_tag = card.select_one(".col-anime-studio")
        rating_tag = card.select_one(".col-anime-rating")
        status_tag = card.select_one(".col-anime-status")

        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag.get("href", "") if title_tag else ""
        thumb = thumb_tag.get("src", "") if thumb_tag else ""
        studio = studio_tag.get_text(strip=True) if studio_tag else ""
        rating = rating_tag.get_text(strip=True) if rating_tag else ""
        status = status_tag.get_text(strip=True) if status_tag else ""
        slug = link.rstrip("/").split("/")[-1] if link else ""

        items.append({
            "title": title,
            "slug": slug,
            "url": link,
            "thumb": thumb,
            "studio": studio,
            "rating": rating,
            "status": status,
        })

    pagination = {}
    prev_page = soup.select_one(".pagination .prev a")
    next_page = soup.select_one(".pagination .next a")
    pagination["prev"] = prev_page.get("href", "") if prev_page else None
    pagination["next"] = next_page.get("href", "") if next_page else None

    return {"anime": items, "pagination": pagination}
