from fastapi import APIRouter, UploadFile, File, HTTPException
from .models import UploadResponse, ResultsResponse, DetectionResult
from .services import save_upload, store_results, get_results
from pydantic import BaseModel

router = APIRouter(prefix="/api")


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4')):
        raise HTTPException(status_code=400, detail="Geçersiz dosya türü.")
    job_id = await save_upload(file)
    return UploadResponse(jobId=job_id)


@router.get("/results/{job_id}", response_model=ResultsResponse)
async def read_results(job_id: str):
    result_data = get_results(job_id)
    return ResultsResponse(
        results=result_data["results"],
        status=result_data["status"],
        message=None
    )


# ✅ Sadece bu tanım yeterli!
class IngestRequest(BaseModel):
    jobId: str
    label: str
    confidence: float


@router.post("/ingest")
async def ingest_results(payload: IngestRequest):
    print("n8n'den veri geldi:", payload)

    result = DetectionResult(
        type=payload.label,
        coords=(0, 0, 100, 100),
        thumbnail=f"/storage/{payload.jobId}.jpg"
    )

    store_results(payload.jobId, [result])
    return {"message": "Sonuç kaydedildi"}
