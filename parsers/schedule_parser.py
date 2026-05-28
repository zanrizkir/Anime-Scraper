from bs4 import BeautifulSoup


def parse_schedule(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    schedule = {}
    day_blocks = soup.select(".kglist321")

    for block in day_blocks:
        day_tag = block.select_one("h2")
        if not day_tag:
            continue
        day = day_tag.get_text(strip=True).lower()
        animes = []
        for item in block.select("li"):
            a_tag = item.select_one("a")
            if not a_tag:
                continue
            link = a_tag.get("href", "")
            title = a_tag.get_text(strip=True)
            slug = link.rstrip("/").split("/")[-1]
            animes.append({"title": title, "slug": slug, "url": link})
        schedule[day] = animes

    return schedule
