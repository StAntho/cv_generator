import streamlit as st
import os, requests, httpx
from dotenv import load_dotenv
from utils.text import text_to_list
from api_client import CVApiClient
from services.cv_service import (
    candidate_to_form_data,
    validate_cv,
    form_data_to_payload
)
from components.cv_form import cv_form

st.set_page_config(
    page_title="cv generator",
    page_icon="📄",
)

st.title("CV Generator")


# === API ===
load_dotenv()
API_URL = os.getenv("STREAMLIT_URL_API")

client = CVApiClient(API_URL)

candidates = client.get_candidates()


# === CANDIDATE SELECTION === 

selected_name = st.selectbox(
    "Select a candidate",
    [candidate["name"] for candidate in candidates],
    index=None,
    placeholder="Select a candidate or enter a new one",
    accept_new_options=True,
)

selected_candidate = next(
    (candidate for candidate in candidates if candidate["name"] == selected_name),
    None,
)

is_existing_candidate = selected_candidate is not None


initial_data = candidate_to_form_data(selected_candidate)
submitted, form_data = cv_form(initial_data, is_existing_candidate)


if submitted:

    validate_cv(form_data)

    payload = form_data_to_payload(form_data)

    try:
        with st.spinner("Generating your CV..."):
            pdf_bytes, filename = client.generate_cv(payload)

            st.session_state["generated_cv"] = {
                    "content": pdf_bytes,
                    "filename": filename,
                }
            
            st.success("CV generated successfully.")

    except httpx.TimeoutException:
        st.error("The API request timed out.")

    except httpx.HTTPStatusError as exc:
        st.error(
            f"FastAPI returned {exc.response.status_code}: "
            f"{exc.response.text}"
        )

    except httpx.RequestError as exc:
        st.error(f"Connection error: {exc}")

    except Exception as exc:
        st.error(f"Unexpected error: {exc}")

generated_cv = st.session_state.get("generated_cv")

if generated_cv:
    st.download_button(
        "Download CV",
        data=generated_cv["content"],
        file_name=generated_cv["filename"],
        mime="application/pdf",
        type="primary",
    )