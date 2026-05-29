from bs4 import BeautifulSoup
import re


def parse_episode(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # ---------- Basic Info ----------
    # Primary: .jdlrx h1 (consistent with anime detail page)
    title_tag = (
        soup.select_one(".jdlrx h1")
        or soup.select_one("h1.entry-title")
        or soup.select_one(".posttl")
        or soup.select_one("h1")
    )
    title = title_tag.get_text(strip=True) if title_tag else ""

    # ---------- Stream Mirrors (iframes / embed URLs) ----------
    stream_mirrors = []

    # Mirror list — buttons with data-content containing encoded iframe HTML
    for btn in soup.select(".mirrorstream ul li a"):
        data_content = btn.get("data-content", "")
        if data_content:
            try:
                inner = BeautifulSoup(data_content, "html.parser")
                iframe = inner.find("iframe")
                if iframe:
                    stream_mirrors.append({
                        "server": btn.get_text(strip=True),
                        "embed_url": iframe.get("src", ""),
                    })
            except Exception:
                pass

    # Fallback: grab all iframes directly from page
    if not stream_mirrors:
        for iframe in soup.select("iframe"):
            src = iframe.get("src", "")
            if src:
                stream_mirrors.append({"server": "default", "embed_url": src})

    # ---------- Download Links ----------
    download_links = []

    # Otakudesu groups download by quality blocks
    for quality_block in soup.select(".download ul"):
        quality_tag = quality_block.find_previous(
            lambda t: t.name in ("strong", "b", "span", "p")
            and t.get_text(strip=True)
            and re.search(r"(360|480|720|1080)", t.get_text(strip=True))
        )
        quality = quality_tag.get_text(strip=True) if quality_tag else "unknown"

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

    # If structured blocks not found, try simple approach
    if not download_links:
        resolutions = {}
        for a_tag in soup.select(".download a"):
            text = a_tag.get_text(strip=True)
            href = a_tag.get("href", "")
            res_match = re.search(r"(360|480|720|1080)p?", text, re.IGNORECASE)
            res = res_match.group(0) if res_match else "unknown"
            if res not in resolutions:
                resolutions[res] = []
            resolutions[res].append({"server": text, "url": href})
        for res, links in resolutions.items():
            download_links.append({"quality": res, "links": links})

    return {
        "title": title,
        "stream_mirrors": stream_mirrors,
        "download_links": download_links,
    }
