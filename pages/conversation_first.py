import streamlit as st

from components.layout import page_header
from content.prompt_examples import CONVERSATION_FIELDS, suggested_prompt


def render() -> None:
    page_header("Conversation-first Workflow", "Clarify goal, context, constraints, progress, and output before work begins.")

    with st.form("conversation_first_form"):
        values = {}
        for key, label in CONVERSATION_FIELDS:
            values[key] = st.text_area(label, height=80)
        submitted = st.form_submit_button("Generate Static Summary")

    if submitted:
        st.subheader("Shared Understanding")
        st.write(values.get("build_goal") or "No build goal provided yet.")

        st.subheader("Current Stage")
        st.write("Planning / alignment" if not values.get("progress") else "In progress")

        st.subheader("Main Blocker")
        st.write(values.get("blocker") or "No blocker specified.")

        st.subheader("Suggested Next Step")
        st.write("Review the summary, tighten the MVP scope, then ask for one concrete implementation task.")

        st.subheader("Suggested Better Prompt")
        st.code(suggested_prompt(values), language="text")
    else:
        st.info("Fill the form to generate a local static summary. No API call will be made.")
