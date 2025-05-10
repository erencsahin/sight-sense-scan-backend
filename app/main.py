from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from .routes import router

app = FastAPI(title="Traffic Sign Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev sunucusu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent
frontend_dir = BASE_DIR / "frontend_dist"
app.mount(
    "/",
    StaticFiles(directory=str(frontend_dir), html=True),
    name="frontend"
)
# API router
app.include_router(router)

