from sqlmodel import Session, select
from models.candidate import Candidate
from models.industry import Industry
from models.skill import Skill, CandidateIndustrySkill
from schemas.generator import CandidateList
from schemas.data_populate import IndustryList, CandidateIndustrySkillCreate


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


def create_skill(
    session: Session,
    data: CandidateIndustrySkillCreate,
) -> CandidateIndustrySkill:

    skill_name = data.skill.strip()

    skill = session.exec(
        select(Skill).where(
            Skill.name == skill_name
        )
    ).first()

    if skill is None:
        skill = Skill(
            name=data.skill,
        )

        session.add(skill)
        session.flush()

    candidate_industry_skill = CandidateIndustrySkill(
        candidate_id=data.candidate_id,
        industry_id=data.industry_id,
        skill_id=skill.id,
        section_key=data.section_key,
    )

    session.add(candidate_industry_skill)
    session.commit()
    session.refresh(candidate_industry_skill)

    return candidate_industry_skill