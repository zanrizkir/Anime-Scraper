from bs4 import BeautifulSoup


def parse_search(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")

    results = []
    for item in soup.select(".chivsrc ul li"):
        img_tag = item.select_one("img")
        title_tag = item.select_one("h2 a")
        genre_tags = item.select("h3:nth-of-type(1) a")
        status_tag = item.select_one("h3:nth-of-type(2)")

        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag.get("href", "") if title_tag else ""
        thumb = img_tag.get("src", "") if img_tag else ""
        genres = [g.get_text(strip=True) for g in genre_tags]
        status_text = status_tag.get_text(strip=True) if status_tag else ""
        slug = link.rstrip("/").split("/")[-1] if link else ""

        results.append({
            "title": title,
            "slug": slug,
            "url": link,
            "thumb": thumb,
            "genres": genres,
            "status": status_text,
        })

    return results
