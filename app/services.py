import uuid
import os
import aiofiles
import httpx
from fastapi import UploadFile
from typing import List
from .models import DetectionResult

# Yüklemelerin kaydedileceği klasör
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)


async def save_upload(file: UploadFile) -> str:
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    dest = os.path.join(STORAGE_DIR, f"{job_id}{ext}")
    async with aiofiles.open(dest, 'wb') as out:
        await out.write(await file.read())

    # → n8n webhook’unuza tetikleme
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:5678/webhook/traffic-sign-workflow",
            json={"jobId": job_id, "filePath": dest}
        )

    return job_id

async def get_mock_results(job_id: str) -> List[DetectionResult]:
    """
    Henüz gerçek işleme eklenmediği için mock veri döndüren fonksiyon.
    """
    return [
        DetectionResult(
            type="Dur işareti",
            coords=(10, 20, 100, 120),
            thumbnail=f"/storage/{job_id}.jpg"
        )
    ]
