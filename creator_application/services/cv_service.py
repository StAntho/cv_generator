import streamlit as st
from utils.text import text_to_list
from .default_template_form import DEFAULT_CV
from api_client import CVApiClient
from dotenv import load_dotenv
import os


# === API ===
load_dotenv()
API_URL = os.getenv("STREAMLIT_URL_API")

client = CVApiClient(API_URL)

def candidate_to_form_data(
    candidate: dict | None,
    skills: list[dict] | None = None,
) -> dict:
    if not candidate:
        return DEFAULT_CV.copy()

    sections = [
        section.copy()
        for section in candidate.get(
            "sections",
            DEFAULT_CV["sections"],
        )
    ]

    if skills:
        skill_ids = [skill["skill_id"] for skill in skills]
        
        skills_db = client.get_skills()
    
        skills_by_id = {
            skill["id"]: skill
            for skill in skills_db
        }
    
        selected_skills = [
            skills_by_id[skill_id]
            for skill_id in skill_ids
            if skill_id in skills_by_id
        ]
    
        for section in sections:
            if section["key"] == "key_skills":
                section["items"] = selected_skills

    return {
        "personal_info": {
            "name": candidate.get("name", ""),
            "phone": candidate.get("phone", ""),
            "email": candidate.get("email", ""),
            "whv": candidate.get("whv", ""),
        },
        "availability": candidate.get("availability", []),
        "sections": sections,
    }


def form_data_to_payload(data: dict) -> dict:
    return {
        "personal_info": {
            "name": data["personal_info"]["name"].strip(),
            "phone": data["personal_info"]["phone"].strip(),
            "email": data["personal_info"]["email"].strip(),
            "whv": data["personal_info"]["whv"].strip(),
        },
        "availability": data["availability"],
        "sections": {
            section["title"].strip(): text_to_list(section["items"])
            for section in data["sections"]
            if section["title"].strip()
        },
    }

def validate_cv(data: dict) -> None:
    personal_info = data["personal_info"]

    if not personal_info["name"].strip():
        st.error("Name is required.")
        st.stop()

    if not personal_info["phone"].strip():
        st.error("Phone is required.")
        st.stop()

    if not personal_info["email"].strip():
        st.error("Email is required.")
        st.stop()

    if not personal_info["whv"].strip():
        st.error("Visa number is required.")
        st.stop()
