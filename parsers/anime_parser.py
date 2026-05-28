from bs4 import BeautifulSoup


def parse_anime_detail(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # ---------- Metadata ----------
    title = ""
    title_tag = soup.select_one(".infozingle b")  # first <b> inside infozingle
    if not title_tag:
        title_tag = soup.select_one("h1.entry-title")
    if title_tag:
        title = title_tag.get_text(strip=True)

    thumb_tag = soup.select_one(".fotoanime img")
    thumb = thumb_tag.get("src", "") if thumb_tag else ""

    synopsis_tag = soup.select_one(".sinopc")
    synopsis = synopsis_tag.get_text(strip=True) if synopsis_tag else ""

    info = {}
    for row in soup.select(".infozingle p"):
        parts = row.get_text(separator=":", strip=True).split(":")
        if len(parts) >= 2:
            key = parts[0].strip().lower().replace(" ", "_")
            value = ":".join(parts[1:]).strip()
            info[key] = value

    genre_tags = soup.select(".infozingle .genres-anime a")
    genres = [g.get_text(strip=True) for g in genre_tags]

    # ---------- Episode List ----------
    episodes = []
    for ep_item in soup.select("#episodelist li"):
        a_tag = ep_item.select_one("a")
        date_tag = ep_item.select_one(".zeebr")
        if not a_tag:
            continue
        link = a_tag.get("href", "")
        ep_title = a_tag.get_text(strip=True)
        date = date_tag.get_text(strip=True) if date_tag else ""
        slug = link.rstrip("/").split("/")[-1]
        episodes.append({
            "title": ep_title,
            "slug": slug,
            "url": link,
            "date": date,
        })

    # Batch download link
    batch_tag = soup.select_one(".batchlink a")
    batch_url = batch_tag.get("href", "") if batch_tag else ""
    batch_slug = batch_url.rstrip("/").split("/")[-1] if batch_url else ""

    return {
        "title": title,
        "thumb": thumb,
        "synopsis": synopsis,
        "info": info,
        "genres": genres,
        "episodes": episodes,
        "batch": {"slug": batch_slug, "url": batch_url},
    }
