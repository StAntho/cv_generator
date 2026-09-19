from pathlib import Path
from fastapi import HTTPException
from fpdf import FPDF
from schemas.generator import GenerateRequest
from structure_builder.simple_structure import CVBuilder

class CVGeneratorService:
    GENERATED_DIR = Path("generations")

    def __init__(
        self
    ):
        self.GENERATED_DIR.mkdir(exist_ok=True)

    def generate(self, payload: GenerateRequest) -> dict:
        print(payload)
        id  = payload.id
        availability = payload.availability

        pdf = CVBuilder()
        pdf.center_text(id.name, size=18, bold=True)
        pdf.center_text(f'whv number: {id.whv}', size=15, bold=True)
        pdf.center_text(id.phone, size=15, bold=True)
        pdf.center_text(id.email, size=15, bold=True, color=(0, 0, 255))

        for i, val in enumerate(availability):
            pdf.center_text(val, color=(255, 0, 0))

        try:
            pdf.output(self.GENERATED_DIR / f"cv_{id.name}.pdf")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
