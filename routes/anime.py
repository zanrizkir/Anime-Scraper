from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.anime_parser import parse_anime_detail
from config import BASE_URL

router = APIRouter()


@router.get("/anime/{slug}")
async def get_anime_detail(slug: str):
    url = f"{BASE_URL}/anime/{slug}/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_anime_detail(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    if not data.get("title"):
        raise HTTPException(status_code=404, detail="Anime not found")

    return {"status": True, "message": "Success", "data": data}
