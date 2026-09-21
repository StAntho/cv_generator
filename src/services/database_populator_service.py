from sqlmodel import Session
from models.candidate import Candidate
from schemas.generator import CandidateList


def create_candidate(
    session: Session,
    data: CandidateList,
) -> Candidate:
    
    candidate = Candidate(
        name=data.name,
        phone=data.phone,
        email=data.email,
        whv=data.whv,
    )

    session.add(candidate)
    session.commit()
    session.refresh(candidate)

    return candidate