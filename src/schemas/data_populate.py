from pydantic import BaseModel

class CandidateRead(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    whv: str