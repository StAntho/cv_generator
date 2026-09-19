import streamlit as st
import os, requests
from dotenv import load_dotenv

st.set_page_config(
    page_title="cv generator",
    page_icon="📄",
)

st.title("CV Generator")

# === Init session state ===
if "id" not in st.session_state:
    st.session_state.id = []
if "availabilities" not in st.session_state:
    st.session_state.availabilities = []

# === API ===
load_dotenv()
URL_GENERATE_API = f"{os.getenv('STREAMLIT_URL_API')}cv_generate/generate"

st.markdown("#### Your ID")
name_query = st.text_input("Your names (ex: John Doe)")
phone_query = st.text_input("Your phone number", type="phone")
email_query = st.text_input("Your email", type="email")
whv_query = st.text_input("Your visa number")

st.markdown("#### Availabilities")
availability = st.multiselect("Multi", ["Availability", "Immediate Start", "Monday to Friday (am/pm)", "Weekends"])

if name_query and phone_query and email_query and whv_query:
    st.session_state.id = [name_query, phone_query, email_query, whv_query]
if availability:
    st.session_state.availabilities = [availability]

st.write(st.session_state.id)
st.write(st.session_state.availabilities)
payload = {
    "id": {
        "name": st.session_state.id[0],
        "phone": st.session_state.id[1],
        "email": st.session_state.id[2],
        "whv": st.session_state.id[3],
    },
    "availability": st.session_state.availabilities[0],
}
if st.session_state.id and st.session_state.availabilities and st.button("Generate the CV"):
    response = requests.post(
        URL_GENERATE_API,
        json=payload
    )


st.write("STATUS:", response.status_code)
st.write("RESPONSE:", response.text)