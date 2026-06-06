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
            const barId = "cogniloop-selection-ask-bar";
            const styleId = "cogniloop-selection-ask-style";
            let lastSelectedText = "";
            let selectionTimer = null;

            let style = parentDoc.getElementById(styleId);
            if (!style) {{
                style = parentDoc.createElement("style");
                style.id = styleId;
                parentDoc.head.appendChild(style);
            }}
            style.textContent = `
                #${{barId}} {{
                    position: fixed;
                    z-index: 2147483647;
                    display: none;
                    align-items: center;
                    gap: 0.45rem;
                    width: max-content;
                    max-width: min(320px, calc(100vw - 2rem));
                    padding: 0.42rem 0.48rem;
                    border: 1px solid rgba(63, 185, 80, 0.72);
                    border-radius: 999px;
                    background: rgba(13, 17, 23, 0.96);
                    color: #ffffff;
                    font: 700 12px/1.2 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.34);
                    backdrop-filter: blur(8px);
                }}
                #${{barId}} .cogniloop-selection-preview {{
                    max-width: 145px;
                    color: #c9d1d9;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    font-weight: 600;
                }}
                #${{barId}} a {{
                    display: inline-flex;
                    align-items: center;
                    border: 1px solid rgba(63, 185, 80, 0.72);
                    border-radius: 999px;
                    background: #238636;
                    color: #ffffff;
                    padding: 0.42rem 0.58rem;
                    font-weight: 800;
                    text-decoration: none;
                    cursor: pointer;
                    white-space: nowrap;
                }}
                #${{barId}} a:hover {{
                    background: #2ea043;
                    color: #ffffff;
                }}
            `;

            let bar = parentDoc.getElementById(barId);
            if (!bar) {{
                bar = parentDoc.createElement("div");
                bar.id = barId;
                bar.innerHTML = `
                    <div class="cogniloop-selection-preview" data-role="preview"></div>
                    <a href="#" data-role="ask">Ask Assistant</a>
                `;
                parentDoc.body.appendChild(bar);
            }}

            function selectedText() {{
                const selection = parentWindow.getSelection() || parentDoc.getSelection();
                if (!selection || selection.rangeCount === 0) return "";
                return selection.toString().replace(/\\s+/g, " ").trim();
            }}

            function hideBar() {{
                bar.style.display = "none";
            }}

            function updateBar() {{
                const text = selectedText();
                if (!text || text.length < 2) {{
                    hideBar();
                    return;
                }}

                lastSelectedText = text;
                const preview = bar.querySelector('[data-role="preview"]');
                preview.textContent = text.length > 36 ? text.slice(0, 36) + "..." : text;

                const selection = parentWindow.getSelection() || parentDoc.getSelection();
                let left = parentWindow.innerWidth - 440;
                let top = parentWindow.innerHeight - 110;
                if (selection && selection.rangeCount > 0) {{
                    const rect = selection.getRangeAt(0).getBoundingClientRect();
                    if (rect && (rect.width || rect.height)) {{
                        left = rect.left + rect.width / 2 - 170;
                        top = rect.top - 72;
                        if (top < 12) {{
                            top = rect.bottom + 12;
                        }}
                    }}
                }}

                const targetUrl = new URL(parentWindow.location.href);
                targetUrl.searchParams.set("ask_page", pageKey);
                targetUrl.searchParams.set("ask_selection", text.slice(0, 1600));
                targetUrl.searchParams.set("ask_ts", Date.now().toString());
                targetUrl.hash = "cogniloop-contextual-assistant";
                bar.querySelector('[data-role="ask"]').setAttribute("href", targetUrl.toString());

                left = Math.min(Math.max(left, 12), parentWindow.innerWidth - 324);
                top = Math.min(Math.max(top, 12), parentWindow.innerHeight - 64);
                bar.style.left = `${{left}}px`;
                bar.style.top = `${{top}}px`;
                bar.style.display = "inline-flex";
            }}

            bar.querySelector('[data-role="ask"]').onclick = function (event) {{
                event.stopPropagation();
            }};

            if (parentWindow.__cogniloopSelectionHandler) {{
                parentDoc.removeEventListener("mouseup", parentWindow.__cogniloopSelectionHandler);
                parentDoc.removeEventListener("keyup", parentWindow.__cogniloopSelectionHandler);
                parentDoc.removeEventListener("selectionchange", parentWindow.__cogniloopSelectionHandler);
            }}
            if (parentWindow.__cogniloopSelectionScrollHandler) {{
                parentDoc.removeEventListener("scroll", parentWindow.__cogniloopSelectionScrollHandler, true);
            }}

            parentWindow.__cogniloopSelectionHandler = function () {{
                if (selectionTimer) {{
                    parentWindow.clearTimeout(selectionTimer);
                }}
                hideBar();
                selectionTimer = parentWindow.setTimeout(updateBar, 500);
            }};
            parentWindow.__cogniloopSelectionScrollHandler = updateBar;

            parentDoc.addEventListener("mouseup", parentWindow.__cogniloopSelectionHandler);
            parentDoc.addEventListener("keyup", parentWindow.__cogniloopSelectionHandler);
            parentDoc.addEventListener("selectionchange", parentWindow.__cogniloopSelectionHandler);
            parentDoc.addEventListener("scroll", parentWindow.__cogniloopSelectionScrollHandler, true);
            updateBar();
        }})();
        </script>
        """,
        height=1,
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
            st.toast("Selected text added to Ask Assistant.")

    st.divider()
    st.markdown("<span id='cogniloop-contextual-assistant'></span>", unsafe_allow_html=True)
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
