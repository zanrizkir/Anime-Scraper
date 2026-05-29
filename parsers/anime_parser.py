from bs4 import BeautifulSoup


def parse_anime_detail(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # ---------- Title ----------
    # Primary: .jdlrx h1 (page heading)
    title = ""
    title_tag = soup.select_one(".jdlrx h1")
    if title_tag:
        title = title_tag.get_text(strip=True)
        # Remove trailing "Sub Indo" if present
        if title.endswith("Sub Indo"):
            title = title[:-8].strip()

    # ---------- Thumbnail ----------
    thumb_tag = soup.select_one(".fotoanime img")
    thumb = thumb_tag.get("src", "") if thumb_tag else ""

    # ---------- Synopsis ----------
    synopsis_tag = soup.select_one(".sinopc")
    synopsis = synopsis_tag.get_text(strip=True) if synopsis_tag else ""

    # ---------- Info (metadata rows) ----------
    info = {}
    for row in soup.select(".infozingle p"):
        b_tag = row.select_one("b")
        if not b_tag:
            continue
        key = b_tag.get_text(strip=True).lower().replace(" ", "_")

        # Get full text from <span>, remove the key label
        span = row.select_one("span")
        if span:
            full_text = span.get_text(strip=True)
            value = full_text.replace(b_tag.get_text(strip=True), "", 1).strip(": ")
            info[key] = value

    # ---------- Genres ----------
    # Genre links have rel="tag" attribute
    genre_tags = soup.select(".infozingle a[rel='tag']")
    # Fallback: all links inside infozingle pointing to /genres/
    if not genre_tags:
        genre_tags = [a for a in soup.select(".infozingle a")
                      if "/genres/" in a.get("href", "")]
    genres = [g.get_text(strip=True) for g in genre_tags]

    # ---------- Episode List ----------
    # Class selector .episodelist (NOT id #episodelist)
    episodes = []
    for ep_item in soup.select(".episodelist ul li"):
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

    # ---------- Batch download link ----------
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
