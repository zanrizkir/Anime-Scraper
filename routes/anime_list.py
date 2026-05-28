from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.list_parser import parse_anime_list
from config import BASE_URL

router = APIRouter()


@router.get("/ongoing/{page}")
async def get_ongoing(page: int = 1):
    url = f"{BASE_URL}/ongoing-anime/page/{page}/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_anime_list(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    return {"status": True, "message": "Success", "data": data}


@router.get("/completed/{page}")
async def get_completed(page: int = 1):
    url = f"{BASE_URL}/complete-anime/page/{page}/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_anime_list(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    return {"status": True, "message": "Success", "data": data}
