import json

import streamlit as st
import streamlit.components.v1 as components

from utils.assistant_runtime import (
    format_recall_results,
    key_status,
    recall_answer,
    user_friendly_error,
)
from utils.qa_history import add_qa_entry, history_markdown, load_qa_history


def inject_selection_assistant(page_key: str) -> None:
    page_key_json = json.dumps(page_key)
    components.html(
        f"""
        <script>
        (function () {{
            const pageKey = {page_key_json};
            const parentDoc = window.parent.document;
            const parentWindow = window.parent;
            const buttonId = "cogniloop-selection-ask";
            const styleId = "cogniloop-selection-ask-style";

            if (!parentDoc.getElementById(styleId)) {{
                const style = parentDoc.createElement("style");
                style.id = styleId;
                style.textContent = `
                    #${{buttonId}} {{
                        position: fixed;
                        z-index: 2147483647;
                        display: none;
                        align-items: center;
                        gap: 0.35rem;
                        padding: 0.55rem 0.7rem;
                        border: 1px solid rgba(63, 185, 80, 0.72);
                        border-radius: 999px;
                        background: #238636;
                        color: #ffffff;
                        font: 700 13px/1.1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.34);
                        cursor: pointer;
                    }}
                    #${{buttonId}}:hover {{
                        background: #2ea043;
                    }}
                `;
                parentDoc.head.appendChild(style);
            }}

            let button = parentDoc.getElementById(buttonId);
            if (!button) {{
                button = parentDoc.createElement("button");
                button.id = buttonId;
                button.type = "button";
                button.textContent = "Ask Assistant";
                parentDoc.body.appendChild(button);
            }}

            function selectedText() {{
                const selection = parentWindow.getSelection();
                if (!selection || selection.rangeCount === 0) return "";
                return selection.toString().replace(/\\s+/g, " ").trim();
            }}

            function hideButton() {{
                button.style.display = "none";
            }}

            function showButton() {{
                const text = selectedText();
                if (!text || text.length < 2) {{
                    hideButton();
                    return;
                }}

                const selection = parentWindow.getSelection();
                const range = selection.getRangeAt(0);
                const rect = range.getBoundingClientRect();
                if (!rect || (!rect.width && !rect.height)) {{
                    hideButton();
                    return;
                }}

                const left = Math.min(
                    Math.max(rect.left + rect.width / 2 - 58, 12),
                    parentWindow.innerWidth - 132
                );
                const top = Math.max(rect.top - 46, 12);
                button.style.left = `${{left}}px`;
                button.style.top = `${{top}}px`;
                button.style.display = "inline-flex";
            }}

            button.onclick = function () {{
                const text = selectedText();
                if (!text) return;

                const url = new URL(parentWindow.location.href);
                url.searchParams.set("ask_page", pageKey);
                url.searchParams.set("ask_selection", text.slice(0, 1600));
                url.searchParams.set("ask_ts", Date.now().toString());
                parentWindow.location.href = url.toString();
            }};

            if (parentWindow.__cogniloopSelectionHandler) {{
                parentDoc.removeEventListener("mouseup", parentWindow.__cogniloopSelectionHandler);
                parentDoc.removeEventListener("keyup", parentWindow.__cogniloopSelectionHandler);
            }}
            if (parentWindow.__cogniloopSelectionScrollHandler) {{
                parentDoc.removeEventListener("scroll", parentWindow.__cogniloopSelectionScrollHandler, true);
            }}

            parentWindow.__cogniloopSelectionHandler = function () {{
                setTimeout(showButton, 40);
            }};
            parentWindow.__cogniloopSelectionScrollHandler = hideButton;

            parentDoc.addEventListener("mouseup", parentWindow.__cogniloopSelectionHandler);
            parentDoc.addEventListener("keyup", parentWindow.__cogniloopSelectionHandler);
            parentDoc.addEventListener("scroll", parentWindow.__cogniloopSelectionScrollHandler, true);
        }})();
        </script>
        """,
        height=0,
    )


def render_contextual_assistant(page_key: str) -> None:
    inject_selection_assistant(page_key)
    context_key = f"context_text::{page_key}"
    question_key = f"context_question::{page_key}"
    selected_from_query = ""
    if st.query_params.get("ask_page") == page_key:
        selected_from_query = st.query_params.get("ask_selection", "").strip()
        if selected_from_query:
            st.session_state[context_key] = selected_from_query
            st.session_state.setdefault(
                question_key,
                "What does this selected text mean, and what should I do next?",
            )

    st.divider()
    with st.expander("Ask Assistant About This Page", expanded=bool(selected_from_query)):
        st.caption(
            "Highlight text anywhere on the page, choose Ask Assistant, then confirm your question here. "
            "The Q&A will be saved locally."
        )
        key_ok, key_message = key_status()
        if not key_ok:
            st.warning(key_message)

        selected_text = st.text_area(
            "Selected or copied text",
            height=100,
            placeholder="Paste the text you want to ask about.",
            key=context_key,
        )
        question = st.text_input(
            "Question",
            placeholder="What does this mean, and what should I do next?",
            key=question_key,
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
