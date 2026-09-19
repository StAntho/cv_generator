from fastapi import APIRouter, UploadFile, File, Depends, Form
from schemas.generator import GenerateRequest
from services.generator_service import CVGeneratorService
router = APIRouter(prefix="/cv_generate", tags=["Generator"])

@router.post("/generate")
def generate_cv(
    payload: GenerateRequest,
    service: CVGeneratorService = Depends(CVGeneratorService)
):
    return service.generate(payload)