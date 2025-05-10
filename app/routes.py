from fastapi import APIRouter, UploadFile, File, HTTPException
from .models import UploadResponse,ResultsResponse
from .services import save_upload, get_mock_results

router = APIRouter(prefix="/api")

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # Yalnızca belirli uzantılara izin ver
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4')):
        raise HTTPException(status_code=400, detail="Geçersiz dosya türü.")
    # Dosyayı kaydet, jobId al
    job_id = await save_upload(file)
    return UploadResponse(jobId=job_id)


@router.get("/results/{job_id}", response_model=ResultsResponse)
async def read_results(job_id: str):
    # Gerçek işleme gelince, job durumu için DB veya n8n’dan çekersiniz
    mock = await get_mock_results(job_id)
    return ResultsResponse(
        results=mock,
        status="completed",
        message=None
    )
