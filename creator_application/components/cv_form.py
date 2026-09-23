import streamlit as st

def cv_form(
    initial_data: dict,
    is_existing_candidate: bool,
) -> tuple[bool, dict]:

    personal_info = initial_data["personal_info"]

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

            title = st.text_input(
                f"Section {index + 1} title",
                value=section["title"],
                placeholder="Section title",
                key=f"section_{index}_title",
            )

            items = st.text_area(
                f"Content for {title}",
                value=section["items"],
                placeholder="Enter your information here...",
                key=f"section_{index}_items",
            )

            sections.append({
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

