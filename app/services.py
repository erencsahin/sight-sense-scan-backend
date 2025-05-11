import mimetypes
import uuid
import os
import aiofiles
import httpx

from fastapi import UploadFile
from typing import List
from .models import DetectionResult

job_results = {}

# Yüklemelerin kaydedileceği klasör
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)


async def save_upload(file: UploadFile) -> str:
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    dest = os.path.join(STORAGE_DIR, f"{job_id}{ext}")

    # 1) Dosyayı kaydet
    async with aiofiles.open(dest, 'wb') as out:
        await out.write(await file.read())

    # 2) n8n'e binary dosya + jobId + filePath gönder
    webhook_url = "https://erencsahin.app.n8n.cloud/webhook-test/traffic-sign-workflow"
    try:
        mime_type = mimetypes.guess_type(dest)[0] or "application/octet-stream"
        with open(dest, "rb") as f:
            files = {"file": (os.path.basename(dest), f, mime_type)}
            data = {
                "jobId": job_id,
                "filePath": f"/storage/{job_id}{ext}"
            }
            async with httpx.AsyncClient() as client:
                await client.post(webhook_url, files=files, data=data)
    except Exception as e:
        print(f"⚠️ n8n’e bağlanma hatası: {e}")

    return job_id


def store_results(job_id: str, results: List[DetectionResult]):
    job_results[job_id] = {
        "results": results,
        "status": "completed"
    }


def get_results(job_id: str):
    return job_results.get(job_id, {
        "results": [],
        "status": "processing"
    })
