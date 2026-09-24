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