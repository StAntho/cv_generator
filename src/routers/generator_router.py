from fastapi import APIRouter, UploadFile, File, Depends, Form
from schemas.generator import GenerateRequest
from services.generator_service import CVGeneratorService
from sqlmodel import Session, select
from db.database import get_session

router = APIRouter(prefix="/cv_generate", tags=["Generator"])

@router.post("/generate")
def generate_cv(
    payload: GenerateRequest,
    service: CVGeneratorService = Depends(CVGeneratorService)
):
    return service.generate(payload)


@router.get("/candidates")
def get_candidates(
    session: Session = Depends(get_session),
):
    return CVGeneratorService.get_candidates(session)


@router.get("/candidates/{candidate_id}")
def get_candidate(
    candidate_id: int,
    session: Session = Depends(get_session),
):
    return CVGeneratorService.get_candidate(session, candidate_id)