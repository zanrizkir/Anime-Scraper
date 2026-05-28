from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.episode_parser import parse_episode
from config import BASE_URL

router = APIRouter()


@router.get("/episode/{slug}")
async def get_episode(slug: str):
    url = f"{BASE_URL}/episode/{slug}/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_episode(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse episode: {str(e)}")

    if not data.get("title"):
        raise HTTPException(status_code=404, detail="Episode not found")

    return {"status": True, "message": "Success", "data": data}
