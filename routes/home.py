from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.home_parser import parse_home
from config import BASE_URL

router = APIRouter()


@router.get("/home")
async def get_home():
    try:
        html = await fetch_html(BASE_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_home(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    return {"status": True, "message": "Success", "data": data}
