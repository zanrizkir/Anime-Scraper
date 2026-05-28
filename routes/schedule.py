from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.schedule_parser import parse_schedule
from config import BASE_URL

router = APIRouter()


@router.get("/schedule")
async def get_schedule():
    url = f"{BASE_URL}/jadwal-rilis/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_schedule(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse page: {str(e)}")

    return {"status": True, "message": "Success", "data": data}
