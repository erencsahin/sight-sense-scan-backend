from pydantic import BaseModel
from typing import List, Tuple, Optional


class UploadResponse(BaseModel):
    jobId: str

class DetectionResult(BaseModel):
    type: str
    coords: Tuple[int, int, int, int]
    thumbnail: str

class ResultsResponse(BaseModel):
    results: List[DetectionResult]
    status: str
    message: Optional[str] = None