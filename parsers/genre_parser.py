from bs4 import BeautifulSoup
from config import BASE_URL


def parse_genres(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    genres = []
    for a_tag in soup.select("ul.genres a"):
        name = a_tag.get_text(strip=True)
        link = a_tag.get("href", "")
        # Make relative URLs absolute
        if link.startswith("/"):
            link = BASE_URL + link
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
        eps_tag = card.select_one(".col-anime-eps")
        rating_tag = card.select_one(".col-anime-rating")
        genre_tag = card.select_one(".col-anime-genre")
        date_tag = card.select_one(".col-anime-date")

        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag.get("href", "") if title_tag else ""
        thumb = thumb_tag.get("src", "") if thumb_tag else ""
        studio = studio_tag.get_text(strip=True) if studio_tag else ""
        episodes = eps_tag.get_text(strip=True) if eps_tag else ""
        rating = rating_tag.get_text(strip=True) if rating_tag else ""
        genres = genre_tag.get_text(strip=True) if genre_tag else ""
        date = date_tag.get_text(strip=True) if date_tag else ""
        slug = link.rstrip("/").split("/")[-1] if link else ""

        items.append({
            "title": title,
            "slug": slug,
            "url": link,
            "thumb": thumb,
            "studio": studio,
            "episodes": episodes,
            "rating": rating,
            "genres": genres,
            "date": date,
        })

    # Pagination — uses .pagenavix with a.next / a.prev
    pagination = {}
    prev_page = soup.select_one(".pagenavix a.prev")
    next_page = soup.select_one(".pagenavix a.next")
    pagination["prev"] = prev_page.get("href", "") if prev_page else None
    pagination["next"] = next_page.get("href", "") if next_page else None

    return {"anime": items, "pagination": pagination}
