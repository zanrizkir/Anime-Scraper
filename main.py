import sys
import asyncio

# ── Windows Compatibility Fix ─────────────────────────────────────────────────
# Python <= 3.13 : paksa ProactorEventLoop agar Playwright bisa jalan di Windows
# Python >= 3.14 : ProactorEventLoop sudah jadi default, tidak perlu di-set manual
if sys.platform.startswith("win"):
    ver = sys.version_info
    if (ver.major, ver.minor) < (3, 14):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.home import router as home_router
from routes.anime_list import router as anime_list_router
from routes.schedule import router as schedule_router
from routes.search import router as search_router
from routes.genre import router as genre_router
from routes.anime import router as anime_router
from routes.episode import router as episode_router
from routes.batch import router as batch_router

app = FastAPI(
    title="Otakudesu Scraper API",
    description="REST API for scraping anime data from Otakudesu using Playwright + BeautifulSoup",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
PREFIX = "/api/v1"

app.include_router(home_router,       prefix=PREFIX, tags=["Home"])
app.include_router(anime_list_router, prefix=PREFIX, tags=["Anime List"])
app.include_router(schedule_router,   prefix=PREFIX, tags=["Schedule"])
app.include_router(search_router,     prefix=PREFIX, tags=["Search"])
app.include_router(genre_router,      prefix=PREFIX, tags=["Genre"])
app.include_router(anime_router,      prefix=PREFIX, tags=["Anime Detail"])
app.include_router(episode_router,    prefix=PREFIX, tags=["Episode"])
app.include_router(batch_router,      prefix=PREFIX, tags=["Batch"])


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": True,
        "message": "Otakudesu Scraper API is running By Ozan",
        "docs": "/docs",
    }


# ── Local Dev Entry ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)