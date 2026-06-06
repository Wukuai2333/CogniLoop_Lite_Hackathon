import streamlit as st

from components.layout import page_header


def render() -> None:
    page_header("Customize Your Own Cognee", "Adapt the local demo with your own documents and local API key.")

    st.header("Recommended Flow")
    st.markdown(
        "1. Replace or add files in `/data`.\n"
        "2. Copy `.env.example` to `.env` and add your own API key when AI features are enabled.\n"
        "3. Run a future `ingest.py` script after the static MVP is complete.\n"
        "4. Run the Streamlit app locally.\n"
        "5. Modify the assistant role or prompt for your use case."
    )

    st.header("Example Customizations")
    st.table(
        [
            {"Use Case": "Study assistant", "Materials to Add": "class notes, lecture slides, textbook excerpts"},
            {"Use Case": "Sponsor tool helper", "Materials to Add": "sponsor documentation, API docs, tutorials"},
            {"Use Case": "Legal assistant", "Materials to Add": "legal documents, policy files"},
            {"Use Case": "Startup advisor", "Materials to Add": "business resources, pitch templates"},
            {"Use Case": "Research assistant", "Materials to Add": "papers, notes, datasets"},
        ]
    )

    st.warning("Do not place secrets in `/data`, commit `.env`, or hard-code API keys.")
