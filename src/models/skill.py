from sqlmodel import Field, SQLModel, UniqueConstraint, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.candidate import Candidate
    from models.industry import Industry
    from models.skill import Skill


class Skill(SQLModel, table=True):
    __tablename__ = "skill"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(
        index=True,
        unique=True,
        nullable=False,
    )


class CandidateIndustrySkill(SQLModel, table=True):

    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "industry_id",
            "skill_id",
            name="uq_candidate_industry_skill",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    candidate_id: int = Field(
        foreign_key="candidate.id",
        nullable=False,
        index=True,
    )
    industry_id: int = Field(
        foreign_key="industry.id",
        nullable=False,
        index=True,
    )
    skill_id: int = Field(
        foreign_key="skill.id",
        nullable=False,
        index=True,
    )
    section_key: str = Field(
        nullable=False,
    )

    candidate: "Candidate" = Relationship()
    industry: "Industry" = Relationship()
    skill: "Skill" = Relationship()