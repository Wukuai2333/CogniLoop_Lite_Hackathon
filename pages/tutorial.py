import streamlit as st

from components.layout import page_header
from content.tutorial_content import POSIX_INSTALL, TROUBLESHOOTING_ROWS, WINDOWS_INSTALL


def render() -> None:
    page_header("Static Cognee Tutorial", "Install and verify Cognee without needing an API key.")

    st.header("What is Cognee?")
    st.write(
        "Cognee helps transform documents and data into AI memory. It can ingest materials, organize knowledge, "
        "and support retrieval-based question answering for AI applications."
    )

    st.header("Requirements")
    st.markdown(
        "- Python 3.10-3.14 for Cognee compatibility\n"
        "- `uv` or `pip`\n"
        "- Terminal access\n"
        "- Optional API key for future interactive AI features"
    )

    tab_windows, tab_posix = st.tabs(["Windows", "macOS / Linux"])
    with tab_windows:
        st.code(WINDOWS_INSTALL, language="powershell")
        st.write("If PowerShell blocks activation, run:")
        st.code("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser", language="powershell")
        st.write("Then retry:")
        st.code(".venv\\Scripts\\Activate.ps1", language="powershell")

    with tab_posix:
        st.code(POSIX_INSTALL, language="bash")

    st.header("Test Installation")
    st.code('python -c "import cognee; print(\'Cognee installed successfully\')"', language="bash")
    st.code("Cognee installed successfully", language="text")

    st.header("API Key Setup")
    st.write("Copy `.env.example` to `.env` only when you want to enable future AI companion features.")
    st.code("LLM_API_KEY=your_api_key_here", language="dotenv")
    st.markdown(
        "- Do not commit `.env` to GitHub.\n"
        "- Do not share your API key.\n"
        "- Static tutorial and checklist do not require an API key.\n"
        "- Interactive assistant features will require your own key later."
    )

    st.header("Minimal Cognee Demo")
    st.write("Reserved for the next build: remember, recall, ask a question, and inspect the retrieved answer.")

    st.header("Troubleshooting")
    st.table(
        [
            {"Problem": problem, "Likely Cause": cause, "Suggested Fix": fix}
            for problem, cause, fix in TROUBLESHOOTING_ROWS
        ]
    )
