import streamlit as st

from components.checklist_components import render_reader
from components.layout import page_header
from utils.persistence import load_progress, save_progress


def render_agent_alignment_hint() -> None:
    st.info(
        "Hint: keep your agents on the same page as you. Download your progress Markdown with notes from each step "
        "to create clearer prompts, reduce repeated context, and avoid losing track of decisions."
    )
    if st.button("Show download buttons", key="checklist_export_focus_top"):
        st.session_state["checklist_focus_export"] = True
        st.rerun()


def render() -> None:
    page_header("Task Progress Checklist", "A reading-style progress guide with tasks, checks, and notes.")

    if "saved_progress" not in st.session_state:
        st.session_state.saved_progress = load_progress()

    st.write(
        "Move one substep at a time, add notes under any check, and your progress saves locally as you work."
    )
    render_agent_alignment_hint()

    render_reader(st.session_state.saved_progress)
    save_progress(st.session_state.saved_progress)
