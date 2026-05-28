from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.genre_parser import parse_genres, parse_genre_anime
from config import BASE_URL

router = APIRouter()


@router.get("/genres")
async def get_genres():
    url = f"{BASE_URL}/genre-list/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_genres(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    return {"status": True, "message": "Success", "data": data}


@router.get("/genres/{slug}/{page}")
async def get_genre_anime(slug: str, page: int = 1):
    url = f"{BASE_URL}/genres/{slug}/page/{page}/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_genre_anime(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    return {"status": True, "message": "Success", "data": data}
