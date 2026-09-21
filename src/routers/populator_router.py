from fastapi import APIRouter, UploadFile, File, Depends, Form
from schemas.data_populate import CandidateRead
from schemas.generator import CandidateList
from sqlmodel import Session
from db.database import get_session
from services.database_populator_service import create_candidate

router = APIRouter(prefix="/populate_db", tags=["Generator"])

@router.post("/candidate", response_model=CandidateRead)
def generate_cv(
    data: CandidateList,
    session: Session = Depends(get_session),
):
    return create_candidate(session, data)