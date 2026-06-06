import streamlit as st


def checklist_progress(prefix: str = "checklist::") -> tuple[int, int]:
    keys = [key for key in st.session_state if key.startswith(prefix)]
    total = len(keys)
    completed = sum(1 for key in keys if st.session_state.get(key))
    return completed, total
