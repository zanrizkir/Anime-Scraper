# 🎌 Otakudesu Scraper API

REST API untuk mengambil data anime dari **Otakudesu** menggunakan **FastAPI**, **Playwright** (bypass Cloudflare), dan **BeautifulSoup**.

---

## 📁 Struktur Proyek

```
otakudesu-api/
├── main.py                  ← Entry point FastAPI + Windows ProactorEventLoop fix
├── config.py                ← BASE_URL & konstanta Playwright
├── requirements.txt
├── Dockerfile
├── .dockerignore
│
├── utils/
│   └── browser.py           ← fetch_html() via async_playwright (stealth mode)
│
├── parsers/
│   ├── home_parser.py       ← Ongoing & completed terbaru
│   ├── list_parser.py       ← Daftar anime + pagination
│   ├── schedule_parser.py   ← Jadwal rilis harian
│   ├── search_parser.py     ← Hasil pencarian
│   ├── genre_parser.py      ← Daftar genre & anime per genre
│   ├── anime_parser.py      ← Detail anime + daftar episode
│   ├── episode_parser.py    ← Stream mirrors + link download
│   └── batch_parser.py      ← Link download batch
│
└── routes/
    ├── home.py              → GET /api/v1/home
    ├── anime_list.py        → GET /api/v1/ongoing/{page}
    │                        → GET /api/v1/completed/{page}
    ├── schedule.py          → GET /api/v1/schedule
    ├── search.py            → GET /api/v1/search/{keyword}
    ├── genre.py             → GET /api/v1/genres
    │                        → GET /api/v1/genres/{slug}/{page}
    ├── anime.py             → GET /api/v1/anime/{slug}
    ├── episode.py           → GET /api/v1/episode/{slug}
    └── batch.py             → GET /api/v1/batch/{slug}
```

---

## ⚙️ Setup Lokal

### Prasyarat

- Python **3.10 – 3.14**
- pip

### Instalasi

```bash
# 1. Clone / download project
cd otakudesu-api

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install browser Chromium
python -m playwright install chromium
```

### Menjalankan Server

```bash
# WAJIB: jalankan via python, bukan uvicorn CLI
python main.py
```

> ⚠️ **Windows** — Jangan pakai `uvicorn main:app` langsung dari terminal.
> Playwright butuh `ProactorEventLoop` untuk menjalankan subprocess, dan uvicorn CLI
> akan mengabaikan loop yang sudah di-set. `python main.py` menangani ini secara otomatis.

Server berjalan di: **http://localhost:8000**  
Dokumentasi interaktif: **http://localhost:8000/docs**

---

## 🌐 Daftar Endpoint

Format respons semua endpoint:

```json
{
  "status": true,
  "message": "Success",
  "data": {}
}
```

### 1. `GET /api/v1/home`
Ambil daftar anime ongoing & completed terbaru di halaman utama.

**Response:**
```json
{
  "status": true,
  "message": "Success",
  "data": {
    "ongoing": [
      {
        "title": "Naruto",
        "slug": "naruto",
        "url": "https://otakudesu.cloud/anime/naruto/",
        "thumb": "https://...",
        "episode": "Ep 12",
        "status": "Ongoing"
      }
    ],
    "completed": []
  }
}
```

---

### 2. `GET /api/v1/ongoing/{page}`
Daftar anime ongoing dengan pagination.

| Parameter | Tipe | Contoh |
|-----------|------|--------|
| `page` | integer | `1` |

**Contoh:** `GET /api/v1/ongoing/1`

---

### 3. `GET /api/v1/completed/{page}`
Daftar anime yang sudah tamat dengan pagination.

**Contoh:** `GET /api/v1/completed/2`

---

### 4. `GET /api/v1/schedule`
Jadwal rilis anime per hari dalam seminggu.

**Response:**
```json
{
  "status": true,
  "message": "Success",
  "data": {
    "senin": [{ "title": "...", "slug": "...", "url": "..." }],
    "selasa": [],
    "rabu": [],
    "kamis": [],
    "jumat": [],
    "sabtu": [],
    "minggu": []
  }
}
```

---

### 5. `GET /api/v1/search/{keyword}`
Cari anime berdasarkan kata kunci.

| Parameter | Tipe | Contoh |
|-----------|------|--------|
| `keyword` | string | `naruto` |

**Contoh:** `GET /api/v1/search/naruto`

---

### 6. `GET /api/v1/genres`
Ambil seluruh daftar genre yang tersedia.

**Response:**
```json
{
  "status": true,
  "message": "Success",
  "data": [
    { "name": "Action", "slug": "action", "url": "https://..." },
    { "name": "Comedy", "slug": "comedy", "url": "https://..." }
  ]
}
```

---

### 7. `GET /api/v1/genres/{slug}/{page}`
Daftar anime pada genre tertentu.

| Parameter | Tipe | Contoh |
|-----------|------|--------|
| `slug` | string | `action` |
| `page` | integer | `1` |

**Contoh:** `GET /api/v1/genres/action/1`

---

### 8. `GET /api/v1/anime/{slug}`
Detail lengkap sebuah anime beserta daftar episodenya.

| Parameter | Tipe | Contoh |
|-----------|------|--------|
| `slug` | string | `naruto-sub-indo` |

**Response:**
```json
{
  "status": true,
  "message": "Success",
  "data": {
    "title": "Naruto",
    "thumb": "https://...",
    "synopsis": "...",
    "info": {
      "judul": "Naruto",
      "studio": "Pierrot",
      "status": "Completed"
    },
    "genres": ["Action", "Adventure"],
    "episodes": [
      { "title": "Episode 1", "slug": "naruto-episode-1", "url": "...", "date": "01 Jan 2020" }
    ],
    "batch": { "slug": "naruto-batch", "url": "https://..." }
  }
}
```

---

### 9. `GET /api/v1/episode/{slug}`
Detail satu episode: stream mirrors (iframe) + link download semua resolusi.

| Parameter | Tipe | Contoh |
|-----------|------|--------|
| `slug` | string | `naruto-episode-1-sub-indo` |

**Response:**
```json
{
  "status": true,
  "message": "Success",
  "data": {
    "title": "Naruto Episode 1",
    "stream_mirrors": [
      { "server": "Desustream", "embed_url": "https://desustream.me/embed/..." },
      { "server": "Kuronime",   "embed_url": "https://..." }
    ],
    "download_links": [
      {
        "quality": "720p",
        "links": [
          { "server": "GDrive", "url": "https://..." },
          { "server": "Mega",   "url": "https://..." }
        ]
      },
      {
        "quality": "480p",
        "links": [
          { "server": "GDrive", "url": "https://..." }
        ]
      }
    ]
  }
}
```

---

### 10. `GET /api/v1/batch/{slug}`
Link download batch (semua episode sekaligus) berbagai resolusi.

| Parameter | Tipe | Contoh |
|-----------|------|--------|
| `slug` | string | `naruto-batch-sub-indo` |

---

## 🚨 Error Handling

| HTTP Code | Kondisi |
|-----------|---------|
| `200` | Sukses |
| `404` | Elemen HTML tidak ditemukan / halaman kosong |
| `500` | Playwright gagal fetch URL (timeout, Cloudflare, dsb.) |

Contoh respons error:
```json
{
  "detail": "Failed to fetch page: Timeout 30000ms exceeded."
}
```

---
