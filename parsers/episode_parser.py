from bs4 import BeautifulSoup
import re


def parse_episode(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # ---------- Basic Info ----------
    title_tag = soup.select_one("h1.entry-title") or soup.select_one(".episodeTitle")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # ---------- Stream Mirrors (iframes / embed URLs) ----------
    stream_mirrors = []

    # Mirror list typically inside #embed_holder or .mirrorstream
    mirror_wrapper = soup.select_one("#embed_holder") or soup.select_one(".mirrorstream")
    if mirror_wrapper:
        for btn in mirror_wrapper.select("li .mirrorstream, li"):
            data_content = btn.get("data-content", "")
            if data_content:
                # data-content usually contains encoded iframe HTML
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

    # Otakudesu groups download by quality blocks (.mirrorstream .download or .download-eps)
    for quality_block in soup.select(".download-eps ul, .mirrorstream .download ul"):
        quality_tag = quality_block.find_previous(
            lambda t: t.name in ("strong", "b", "span") and t.get_text(strip=True)
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
        for a_tag in soup.select(".mirrordownload a, .download a"):
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
