import streamlit as st
from utils.text import text_to_list

def cv_form(
    initial_data: dict,
    is_existing_candidate: bool,
) -> tuple[bool, dict]:

    personal_info = initial_data["personal_info"]


    for index, section in enumerate(initial_data["sections"]):

        title_key = f"section_{index}_title"
        items_key = f"section_{index}_items"

        st.session_state[title_key] = section["title"]

        raw_items = section.get("items", "")

        if isinstance(raw_items, list):
            items_value = "\n".join(
                item["name"]
                for item in raw_items
            )
        else:
            items_value = raw_items or ""

        st.session_state[items_key] = items_value


    with st.form("cv_form"):

        st.subheader("Personal information")

        name = st.text_input(
            "Your name",
            value=personal_info["name"],
            placeholder="John Doe",
            disabled=is_existing_candidate,
        )

        phone = st.text_input(
            "Your phone number",
            value=personal_info["phone"],
            placeholder="+33 6 12 34 56 78",
            disabled=is_existing_candidate,
        )

        email = st.text_input(
            "Your email",
            value=personal_info["email"],
            placeholder="john.doe@example.com",
            disabled=is_existing_candidate,
        )

        whv = st.text_input(
            "Your visa number",
            value=personal_info["whv"],
            placeholder="Visa number",
            disabled=is_existing_candidate,
        )

        st.subheader("Availabilities")

        availability = st.multiselect(
            "Select your availabilities",
            [
                "Availability",
                "Immediate Start",
                "Monday to Friday (am/pm)",
                "Weekends",
            ],
            default=initial_data["availability"],
        )

        st.subheader("Skills and experiences")

        sections = []

        for index, section in enumerate(initial_data["sections"]):

            title_key = f"section_{index}_title"
            items_key = f"section_{index}_items"

            title = st.text_input(
                f"Section {index + 1} title",
                key=title_key,
                placeholder="Section title",
            )

            items = st.text_area(
                f"Content for {title}",
                key=items_key,
                placeholder="Enter your information here...",
            )

            sections.append({
                "key": section.get("key"),
                "title": title,
                "items": items,
            })

        submitted = st.form_submit_button(
            "Generate CV",
            type="primary",
        )

    data = {
        "personal_info": {
            "name": name,
            "phone": phone,
            "email": email,
            "whv": whv,
        },
        "availability": availability,
        "sections": sections,
    }

    return submitted, data

