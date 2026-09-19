from pydantic import BaseModel

class GenerateRequest(BaseModel):
    id: IdList
    availability: list[str]

class IdList(BaseModel):
    name: str
    phone: str
    email: str
    whv: str
