import streamlit as st

from components.checklist_components import render_reader
from components.layout import page_header
from utils.persistence import load_progress, save_progress


def render() -> None:
    page_header("Timeline Checklist", "A reading-style progress guide with optional checks and notes.")

    if "saved_progress" not in st.session_state:
        st.session_state.saved_progress = load_progress()

    st.write(
        "Move one substep at a time, add notes under any check, and your progress saves locally as you work."
    )

    if st.button("Resume Saved Position"):
        st.session_state.saved_progress = load_progress()
        st.rerun()

    render_reader(st.session_state.saved_progress)
    save_progress(st.session_state.saved_progress)
