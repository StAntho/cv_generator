from pydantic import BaseModel

class GenerateRequest(BaseModel):
    personal_info: IdList
    availability: list[str]
    sections: dict[str, list[str]]

class IdList(BaseModel):
    name: str
    phone: str
    email: str
    whv: str
