from pydantic import BaseModel

class GenerateRequest(BaseModel):
    personal_info: CandidateList
    availability: list[str]
    sections: dict[str, list[str]]

class CandidateList(BaseModel):
    name: str
    phone: str
    email: str
    whv: str
