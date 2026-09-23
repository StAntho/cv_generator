import streamlit as st
from utils.text import text_to_list
from .default_template_form import DEFAULT_CV

def candidate_to_form_data(candidate: dict | None) -> dict:
    if not candidate:
        return DEFAULT_CV.copy()

    return {
        "personal_info": {
            "name": candidate.get("name", ""),
            "phone": candidate.get("phone", ""),
            "email": candidate.get("email", ""),
            "whv": candidate.get("whv", ""),
        },
        "availability": candidate.get("availability", []),
        "sections": candidate.get("sections", DEFAULT_CV["sections"]),
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
