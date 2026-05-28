from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.search_parser import parse_search
from config import BASE_URL

router = APIRouter()


@router.get("/search/{keyword}")
async def search_anime(keyword: str):
    url = f"{BASE_URL}/?s={keyword}&post_type=anime"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_search(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    if not data:
        return {"status": False, "message": "No results found", "data": []}

    return {"status": True, "message": "Success", "data": data}
