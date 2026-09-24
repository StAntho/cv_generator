from pydantic import BaseModel

class CandidateRead(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    whv: str

class IndustryRead(BaseModel):
    id: int
    name: str

class IndustryList(BaseModel):
    name: str

class SkillRead(BaseModel):
    id: int
    candidate_id: int
    industry_id: int
    skill_id: int
    section_key: str

class SkillList(BaseModel):
    id: int
    name: str

class CandidateIndustrySkillCreate(BaseModel):
    candidate_id: int
    industry_id: int
    skill: str
    section_key: str
    skill: SkillList