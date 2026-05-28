from fastapi import APIRouter, HTTPException
from utils.browser import fetch_html
from parsers.batch_parser import parse_batch
from config import BASE_URL

router = APIRouter()


@router.get("/batch/{slug}")
async def get_batch(slug: str):
    url = f"{BASE_URL}/batch/{slug}/"
    try:
        html = await fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

    try:
        data = parse_batch(html)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to parse batch: {str(e)}")

    if not data.get("title"):
        raise HTTPException(status_code=404, detail="Batch not found")

    return {"status": True, "message": "Success", "data": data}
