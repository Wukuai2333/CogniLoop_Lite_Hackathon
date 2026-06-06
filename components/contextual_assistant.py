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


def context_keys(page_key: str) -> tuple[str, str]:
    return f"context_text::{page_key}", f"context_question::{page_key}"


def capture_selection_request(page_key: str) -> str:
    context_key, question_key = context_keys(page_key)
    if st.query_params.get("ask_page") != page_key:
        return st.session_state.get(f"selection_notice::{page_key}", "")

    selected_text = st.query_params.get("ask_selection", "").strip()
    ask_ts = st.query_params.get("ask_ts", "")
    capture_ts_key = f"selection_capture_ts::{page_key}"
    if not selected_text:
        return st.session_state.get(f"selection_notice::{page_key}", "")

    if st.session_state.get(capture_ts_key) != ask_ts:
        st.session_state[context_key] = selected_text
        st.session_state.setdefault(
            question_key,
            "What does this selected text mean, and what should I do next?",
        )
        st.session_state[capture_ts_key] = ask_ts
        st.session_state[f"selection_notice::{page_key}"] = selected_text
        st.session_state[f"selection_expanded::{page_key}"] = True

    return st.session_state.get(f"selection_notice::{page_key}", "")


def render_selection_capture_banner(page_key: str) -> None:
    selected_text = st.session_state.get(f"selection_notice::{page_key}", "")
    if not selected_text:
        return

    with st.container(border=True):
        st.success("Selected text captured. Review or edit it in Ask Assistant below.")
        preview = selected_text if len(selected_text) <= 260 else f"{selected_text[:260]}..."
        st.caption(preview)
        if st.button("Clear selected text", key=f"clear_selection_notice::{page_key}"):
            context_key, _ = context_keys(page_key)
            st.session_state.pop(context_key, None)
            st.session_state.pop(f"selection_notice::{page_key}", None)
            st.session_state[f"selection_expanded::{page_key}"] = False
            st.rerun()


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
                    gap: 0.65rem;
                    width: max-content;
                    max-width: min(360px, calc(100vw - 2rem));
                    padding: 0.62rem 0.68rem;
                    border: 1px solid rgba(46, 160, 67, 0.78);
                    border-radius: 8px;
                    background: rgba(13, 17, 23, 0.98);
                    color: #ffffff;
                    font: 600 12px/1.25 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.34);
                    backdrop-filter: blur(8px);
                }}
                #${{barId}} .cogniloop-selection-preview {{
                    max-width: 170px;
                    color: #c9d1d9;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    font-weight: 700;
                }}
                #${{barId}} .cogniloop-selection-preview span {{
                    display: block;
                    color: #8b949e;
                    font-size: 0.68rem;
                    font-weight: 600;
                    margin-bottom: 0.15rem;
                }}
                #${{barId}} .cogniloop-selection-preview strong {{
                    display: block;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }}
                #${{barId}} a {{
                    display: inline-flex;
                    align-items: center;
                    border: 1px solid #2ea043;
                    border-radius: 8px;
                    background: #238636;
                    color: #ffffff;
                    padding: 0.5rem 0.68rem;
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
                    <div class="cogniloop-selection-preview"><span>Selected text</span><strong data-role="preview"></strong></div>
                    <a href="#" data-role="ask" style="display:inline-flex;align-items:center;border:1px solid #2ea043;border-radius:8px;background:#238636;color:#ffffff;padding:0.5rem 0.68rem;font-weight:800;text-decoration:none;cursor:pointer;white-space:nowrap;">Ask Assistant</a>
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

            function buildTargetUrl(text) {{
                const targetUrl = new URL(parentWindow.location.href);
                targetUrl.searchParams.set("ask_page", pageKey);
                targetUrl.searchParams.set("ask_selection", text.slice(0, 1600));
                targetUrl.searchParams.set("ask_ts", Date.now().toString());
                targetUrl.hash = "cogniloop-contextual-assistant";
                return targetUrl.toString();
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

                bar.querySelector('[data-role="ask"]').setAttribute("href", buildTargetUrl(text));

                left = Math.min(Math.max(left, 12), parentWindow.innerWidth - 364);
                top = Math.min(Math.max(top, 12), parentWindow.innerHeight - 72);
                bar.style.left = `${{left}}px`;
                bar.style.top = `${{top}}px`;
                bar.style.display = "inline-flex";
            }}

            bar.querySelector('[data-role="ask"]').onclick = function (event) {{
                event.preventDefault();
                event.stopPropagation();
                const text = selectedText() || lastSelectedText;
                if (!text) {{
                    return false;
                }}
                parentWindow.location.assign(buildTargetUrl(text));
                return false;
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
    context_key, question_key = context_keys(page_key)
    selected_from_query = capture_selection_request(page_key)
    expanded = bool(st.session_state.get(f"selection_expanded::{page_key}") or selected_from_query)

    st.divider()
    st.markdown("<span id='cogniloop-contextual-assistant'></span>", unsafe_allow_html=True)
    with st.expander("Ask Assistant About This Page", expanded=expanded):
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
