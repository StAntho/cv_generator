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

candidates = client.get_candidates()
industries = client.get_industries()

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



with st.form("industry_form"):

    st.subheader("Add new regular industry")
    industry = st.text_input("New industry", placeholder="Construction")

    submitted_industry = st.form_submit_button(
        "Add to the database",
        type="primary"
    )

    if submitted_industry:
        if not industry.strip():
            st.error("Industry is required.")
            st.stop()

        payload = {
            "name": industry.strip(),
        }
        try:
            with st.spinner("Recording the new industry..."):
    
                response = client.populate_industry(payload)
    
            result = response
            st.success(f"Industry: {result["name"]} recorded successfully.")
    
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


if candidates is not None and industries is not None:
    section_options = {
        "Key Skills": "key_skills",
        "Work Experiences": "work_experience",
        "Education & Training": "education",
        "Language skills": "languages",
        "References available upon request": "references"
    }
    with st.form("skills_form"):

        st.subheader("Add new skills")
        selected_candidate = st.selectbox(
            "Select a candidate",
            [candidate["name"] for candidate in candidates],
            index=None,
            placeholder="Select a candidate",
        )
        selected_candidate = next(
            (candidate for candidate in candidates if candidate["name"] == selected_candidate),
            None
        )
        selected_industry = st.selectbox(
            "Select an industry",
            [industry["name"] for industry in industries],
            index=None,
            placeholder="Select an industry",
        )
        selected_industry = next(
            (industry for industry in industries if industry["name"] == selected_industry),
            None
        )
        skill = st.text_input(
            "Skill",
            placeholder="Bricklaying",
        )
        section = st.selectbox(
            "CV section",
            section_options,
            index=None,
            placeholder="Select a CV section",
        )
        submitted_skill = st.form_submit_button(
            "Add to the database",
            type="primary"
        )

        if submitted_skill:
            if selected_candidate is None:
                st.error("Candidate is required.")
                st.stop()

            if selected_industry is None:
                st.error("Industry is required.")
                st.stop()

            if not skill.strip():
                st.error("Skill is required.")
                st.stop()

            if section is None:
                st.error("CV section is required.")
                st.stop()

            payload = {
                "candidate_id": selected_candidate["id"],
                "industry_id": selected_industry["id"],
                "skill": skill.strip(),
                "section_key": section_options[section],
            }

            try:
                with st.spinner("Recording the new skill..."):
        
                    response = client.populate_candidate_skill(payload)
        
                result = response
                st.write(result)
                # st.write(result['detail']['input'])
                st.success(f"Skill: {result['skill']['name']} recorded successfully.")
        
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