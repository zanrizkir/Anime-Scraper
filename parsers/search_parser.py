from bs4 import BeautifulSoup


def parse_search(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")

    results = []
    # .chivsrc IS the <ul>, so select direct <li> children
    for item in soup.select("ul.chivsrc > li"):
        img_tag = item.select_one("img")
        title_tag = item.select_one("h2 a")

        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag.get("href", "") if title_tag else ""
        thumb = img_tag.get("src", "") if img_tag else ""
        slug = link.rstrip("/").split("/")[-1] if link else ""

        # Parse .set divs for genres, status, rating
        genres = []
        status_text = ""
        rating = ""
        for set_div in item.select("div.set"):
            b_tag = set_div.select_one("b")
            if not b_tag:
                continue
            label = b_tag.get_text(strip=True).lower()

            if "genre" in label:
                genres = [a.get_text(strip=True) for a in set_div.select("a")]
            elif "status" in label:
                # Extract text after <b>Status</b> :
                status_text = set_div.get_text(strip=True)
                status_text = status_text.replace(b_tag.get_text(strip=True), "", 1).strip(": ")
            elif "rating" in label:
                rating = set_div.get_text(strip=True)
                rating = rating.replace(b_tag.get_text(strip=True), "", 1).strip(": ")

        results.append({
            "title": title,
            "slug": slug,
            "url": link,
            "thumb": thumb,
            "genres": genres,
            "status": status_text,
            "rating": rating,
        })

    return results
