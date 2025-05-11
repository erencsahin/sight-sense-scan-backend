from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routes import router

app = FastAPI(
    title="Traffic Sign Detection API",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1️⃣ API rotalarını önce ekleyin
app.include_router(router)

# 2️⃣ STORAGE ve FRONTEND dizinlerinin kökünü tanımlayın
BASE_DIR = Path(__file__).resolve().parent   # backend/app klasörü
STORAGE_DIR = BASE_DIR / "storage"
FRONTEND_DIR = BASE_DIR / "frontend_dist"

# 3️⃣ "/storage" altından kaydedilen dosyaları servis edin
app.mount(
    "/storage",
    StaticFiles(directory=str(STORAGE_DIR)),
    name="storage",
)

# 4️⃣ Son olarak frontend build'ini kökten mount edin
app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend",
)
