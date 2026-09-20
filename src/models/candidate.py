from sqlmodel import Field, SQLModel

class Candidate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    email: str
    whv: str
