from sqlmodel import Session
from models.candidate import Candidate
from models.industry import Industry
from schemas.generator import CandidateList
from schemas.data_populate import IndustryList


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


def create_industry(
    session: Session,
    data: IndustryList,
) -> Industry:
    
    industry = Industry(
        name=data.name,
    )

    session.add(industry)
    session.commit()
    session.refresh(industry)

    return industry