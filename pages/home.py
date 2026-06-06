import streamlit as st

from components.info_cards import metric_cards, step_card
from components.layout import page_header


def render() -> None:
    page_header("CogniLoop Lite", "A local-first Cognee onboarding companion for hackathon teams.")

    metric_cards(
        [
            ("Mode", "Local"),
            ("API key", "BYOK"),
            ("MVP scope", "Static"),
        ]
    )

    st.write(
        "CogniLoop Lite helps participants understand Cognee, install it locally, follow a guided checklist, "
        "and prepare a conversation-first workflow before asking an AI agent to work."
    )

    col1, col2 = st.columns(2)
    with col1:
        step_card("Start with the tutorial", "Install Cognee, verify the environment, and learn where the API key belongs.")
        step_card("Track progress", "Use the checklist to move from setup to final demo preparation.")
    with col2:
        step_card("Clarify before building", "Use the conversation-first placeholder to turn vague tasks into actionable prompts.")
        step_card("Customize the template", "Replace sample documents, add a local `.env`, and prepare for future ingestion.")

    st.warning("No real Cognee API integration is enabled in this MVP. Static pages and checklist work without an API key.")
