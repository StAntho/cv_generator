from pathlib import Path
from fastapi import HTTPException
from fpdf import FPDF
from schemas.generator import GenerateRequest
from structure_builder.simple_structure import CVBuilder
from sqlmodel import Session, select
from models.candidate import Candidate
from models.industry import Industry
from fastapi.responses import FileResponse

class CVGeneratorService:
    GENERATED_DIR = Path("generations")

    def __init__(
        self
    ):
        self.GENERATED_DIR.mkdir(exist_ok=True)

    def generate(self, payload: GenerateRequest) -> dict:
        print(payload)
        id  = payload.personal_info
        availability = payload.availability
        sections = payload.sections

        pdf = CVBuilder()
        pdf.center_text(id.name, size=18, bold=True)
        pdf.center_text(f'whv number: {id.whv}', size=15, bold=True)
        pdf.center_text(id.phone, size=15, bold=True)
        pdf.center_text(id.email, size=15, bold=True, color=(0, 0, 255))

        for i, val in enumerate(availability):
            pdf.center_text(val, color=(255, 0, 0))

        for i, title in enumerate(sections):
            pdf.h2(title)
            pdf.bullet_list(sections[title])

        try:
            filename = f"cv_{id.name}.pdf"
            output_path = self.GENERATED_DIR / filename

            pdf.output(output_path)

            return FileResponse(
                path=output_path,
                media_type="application/pdf",
                filename=filename,
            )
    
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    def get_candidates(
            session: Session,
    ):        
        statement = select(Candidate)
        candidates = session.exec(statement).all()

        return candidates

    def get_candidate(
            session: Session,
            candidate_id,
    ):
        candidate = session.get(Candidate, candidate_id)
        return candidate

    
    def get_industries(
            session: Session,
    ):        
        statement = select(Industry)
        industries = session.exec(statement).all()

        return industries