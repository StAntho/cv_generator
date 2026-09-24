from sqlmodel import Field, SQLModel

class Industry(SQLModel, table=True):
    __tablename__ = "industry"
    id: int | None = Field(default=None, primary_key=True)
    name: str