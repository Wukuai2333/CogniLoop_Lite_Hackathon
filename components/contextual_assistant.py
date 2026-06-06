import streamlit as st

from utils.assistant_runtime import (
    format_recall_results,
    key_status,
    recall_answer,
    user_friendly_error,
)
from utils.qa_history import add_qa_entry, history_markdown, load_qa_history


def render_contextual_assistant(page_key: str) -> None:
    st.divider()
    with st.expander("Ask Assistant About This Page", expanded=False):
        st.caption(
            "Copy any text from this page into the context box, ask a question, and the Q&A will be saved locally."
        )
        key_ok, key_message = key_status()
        if not key_ok:
            st.warning(key_message)

        selected_text = st.text_area(
            "Selected or copied text",
            height=100,
            placeholder="Paste the text you want to ask about.",
            key=f"context_text::{page_key}",
        )
        question = st.text_input(
            "Question",
            placeholder="What does this mean, and what should I do next?",
            key=f"context_question::{page_key}",
        )

        if st.button("Ask and Save", disabled=not key_ok or not question.strip(), key=f"context_ask::{page_key}"):
            query_parts = []
            if selected_text.strip():
                query_parts.append(f"Context from page:\n{selected_text.strip()}")
            query_parts.append(f"Question:\n{question.strip()}")
            query = "\n\n".join(query_parts)

            with st.status("Querying local Cognee memory...", expanded=True) as status:
                try:
                    results = recall_answer(query)
                    answer = format_recall_results(results)
                    add_qa_entry(page_key, question.strip(), selected_text.strip(), answer)
                    st.success("Saved to Q&A history.")
                    st.write(answer)
                    status.update(label="Q&A saved.", state="complete")
                except Exception as exc:
                    answer = user_friendly_error(exc)
                    add_qa_entry(page_key, question.strip(), selected_text.strip(), answer, status="error")
                    st.error(answer)
                    status.update(label="Assistant query failed.", state="error")

        history = load_qa_history()
        with st.expander(f"Q&A History ({len(history)})", expanded=False):
            if not history:
                st.caption("No Q&A saved yet.")
            for entry in history[:10]:
                st.markdown(f"**{entry['created_at']} - {entry['page']}**")
                st.caption(entry["question"])
                st.write(entry["answer"])
                st.divider()
            st.download_button(
                "Download Q&A History",
                data=history_markdown(history),
                file_name="cogniloop_qa_history.md",
                mime="text/markdown",
                disabled=not history,
            )
