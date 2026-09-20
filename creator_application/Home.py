import streamlit as st
import os, requests, httpx
from dotenv import load_dotenv
from utils.text import text_to_list

st.set_page_config(
    page_title="cv generator",
    page_icon="📄",
)

st.title("CV Generator")

# === API ===
load_dotenv()
URL_GENERATE_API = f"{os.getenv('STREAMLIT_URL_API')}cv_generate/generate"

with st.form("cv_form"):

    st.subheader("Personal information")
    name = st.text_input("Your name", placeholder="John Doe")
    phone = st.text_input("Your phone number", type="phone")
    email = st.text_input("Your email", type="email")
    whv = st.text_input("Your visa number", placeholder="Visa number")

    st.subheader("Availabilities")  
    availability = st.multiselect(
        "Select your availabilities", 
        [
            "Availability", 
            "Immediate Start", 
            "Monday to Friday (am/pm)", 
            "Weekends"
        ]
    )

    st.subheader("Skills and experiences")
    section_1_title = st.text_input("section_1_title", "Key Skills")
    section_1_items = st.text_area(
        f"Content for {section_1_title}",
        placeholder="Python \
                FastAPI \
                Docker"
        )
    
    section_2_title = st.text_input("section_2_title", "Work Experiences")
    section_2_items = st.text_area(
        f"Content for {section_2_title}",
        placeholder="Backend Developer \
        API development"
        )
    
    section_3_title = st.text_input("section_3_title", "Education & Training")
    section_3_items = st.text_area(
        f"Content for {section_3_title}",
        placeholder="Computer Science \
        Software Engineering"
        )
    
    section_4_title = st.text_input("section_4_title", "Language skills")
    section_4_items = st.text_area(
        f"Content for {section_4_title}",
        placeholder="English \
        French"
        )
    
    section_5_title = st.text_input("section_5_title", "References available upon request")
    section_5_items = st.text_area(
        f"Content for {section_5_title}",
        placeholder="Backend Developer \
        API development"
        )
    
    submitted = st.form_submit_button(
        "Generate CV",
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
        "personal_info": {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
            "whv": whv.strip(),
        },
        "availability": availability,
        "sections": {
            section_1_title.strip(): text_to_list(section_1_items),
            section_2_title.strip(): text_to_list(section_2_items),
            section_3_title.strip(): text_to_list(section_3_items),
            section_4_title.strip(): text_to_list(section_4_items),
            section_5_title.strip(): text_to_list(section_5_items),
        },
    }
    st.write(payload)

    try:
        with st.spinner("Generating your CV..."):

            response = httpx.post(
                URL_GENERATE_API,
                json=payload,
                timeout=60.0,
            )

        response.raise_for_status()

        result = response.json()

        st.success(f"CV {result["filename"]} generated successfully.")

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