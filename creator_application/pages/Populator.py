import os, httpx
import streamlit as st
from dotenv import load_dotenv
from utils.text import text_to_list
from api_client import CVApiClient

load_dotenv()
API_URL = os.getenv("STREAMLIT_URL_API")

if not API_URL:
    st.error("STREAMLIT_URL_API is not configured.")
    st.stop()

client = CVApiClient(API_URL)

st.title("Populator database")

with st.form("candidate_form"):

    st.subheader("Add new regular candidate")
    name = st.text_input("Your name", placeholder="John Doe")
    phone = st.text_input("Your phone number", type="phone")
    email = st.text_input("Your email", type="email")
    whv = st.text_input("Your visa number", placeholder="Visa number")

    submitted = st.form_submit_button(
        "Add to the database",
        type="primary"
    )

if submitted:

    if not name.strip():
        st.error("Name is required.")
        st.stop()

    if not phone.strip():
        st.error("Phone number is required.")
        st.stop()

    if not email.strip():
        st.error("Email is required.")
        st.stop()

    if not whv.strip():
        st.error("Visa number is required.")
        st.stop()

    payload = {
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "whv": whv.strip(),
    }

    st.write(payload)

    try:
        with st.spinner("Recording your candidate..."):

            response = client.populate_candidate(payload)

        result = response
        st.success(f"Candidate {result["name"]} recorded successfully.")

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