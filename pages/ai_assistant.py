import streamlit as st

from components.layout import page_header
from utils.assistant_runtime import (
    cognee_status,
    format_recall_results,
    key_status,
    recall_answer,
    remember_demo_documents,
)


def render_optional_notice() -> None:
    st.info(
        "This assistant is a lightweight local test helper. You can skip it completely and still finish the workflow."
    )
    st.caption(
        "Safety boundary: this page does not collect API keys and has no password input. "
        "It only reads a key from your local `.env` or existing environment variables."
    )


def render() -> None:
    page_header("AI Assistant", "Local `.env`-only Cognee test helper for the demo dataset.")
    render_optional_notice()

    key_ok, key_message = key_status()
    cognee_ok, cognee_message = cognee_status()

    col1, col2 = st.columns(2)
    with col1:
        st.success(key_message) if key_ok else st.warning(key_message)
    with col2:
        st.success(cognee_message) if cognee_ok else st.error(cognee_message)

    with st.expander("How to add your key locally", expanded=not key_ok):
        st.write("Create a local `.env` file next to `app.py`. Do not commit it.")
        st.code("LLM_API_KEY=your_api_key_here\nOPENAI_API_KEY=your_api_key_here", language="dotenv")

    disabled = not key_ok or not cognee_ok
    st.subheader("1. Remember local demo documents")
    st.write("This loads Markdown files from `/data` into a small Cognee demo dataset.")
    if st.button("Remember /data documents", disabled=disabled):
        with st.spinner("Asking Cognee to remember local documents..."):
            try:
                st.success(remember_demo_documents())
            except Exception as exc:
                st.error(f"Cognee remember failed: {exc}")

    st.subheader("2. Ask the local test assistant")
    question = st.text_area(
        "Question",
        value="What is CogniLoop Lite and how does it help hackathon participants?",
        height=100,
    )
    if st.button("Ask", disabled=disabled or not question.strip()):
        with st.spinner("Calling Cognee recall..."):
            try:
                results = recall_answer(question.strip())
                st.markdown("### Result")
                st.code(format_recall_results(results), language="text")
            except Exception as exc:
                st.error(f"Cognee recall failed: {exc}")
