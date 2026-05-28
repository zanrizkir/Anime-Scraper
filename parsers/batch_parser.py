from bs4 import BeautifulSoup
import re


def parse_batch(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.select_one("h1.entry-title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    download_links = []

    # Otakudesu batch page groups links in quality sections
    for quality_block in soup.select(".batchlink .download ul, .download-eps ul"):
        quality_heading = quality_block.find_previous(
            lambda t: t.name in ("strong", "b", "h3", "h4") and t.get_text(strip=True)
        )
        quality = quality_heading.get_text(strip=True) if quality_heading else "unknown"

        links = []
        for li in quality_block.select("li"):
            a_tag = li.find("a")
            if a_tag:
                links.append({
                    "server": a_tag.get_text(strip=True),
                    "url": a_tag.get("href", ""),
                })
        if links:
            download_links.append({"quality": quality, "links": links})

    # Fallback: parse all download anchors
    if not download_links:
        resolutions: dict = {}
        for a_tag in soup.select(".batchlink a"):
            text = a_tag.get_text(strip=True)
            href = a_tag.get("href", "")
            res_match = re.search(r"(360|480|720|1080)p?", text, re.IGNORECASE)
            res = res_match.group(0) if res_match else "unknown"
            if res not in resolutions:
                resolutions[res] = []
            resolutions[res].append({"server": text, "url": href})
        for res, links in resolutions.items():
            download_links.append({"quality": res, "links": links})

    return {"title": title, "download_links": download_links}
