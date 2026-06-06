import streamlit as st
import streamlit.components.v1 as components

from components.checklist_components import render_reader
from components.layout import page_header
from utils.persistence import load_progress, save_progress


def render_agent_alignment_hint() -> None:
    components.html(
        """
        <style>
        .agent-hint-card {
            border-radius: 8px;
            background: rgba(31, 111, 235, 0.18);
            color: #58a6ff;
            padding: 1rem 1.1rem;
            font: 500 16px/1.55 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        .agent-hint-card button {
            margin-top: 0.85rem;
            border: 1px solid rgba(88, 166, 255, 0.44);
            border-radius: 8px;
            background: rgba(13, 17, 23, 0.62);
            color: #f0f6fc;
            padding: 0.62rem 0.8rem;
            font-weight: 700;
            cursor: pointer;
        }
        .agent-hint-card button:hover {
            border-color: rgba(88, 166, 255, 0.78);
            background: rgba(31, 111, 235, 0.22);
        }
        </style>
        <div class="agent-hint-card">
            <div>
                Hint: keep your agents on the same page as you. Download your progress Markdown with notes from each
                step to create clearer prompts, reduce repeated context, and avoid losing track of decisions.
            </div>
            <button id="checklist-export-focus-button" type="button">Show download buttons</button>
        </div>
        <script>
        const button = document.getElementById("checklist-export-focus-button");
        if (button) {
            button.addEventListener("click", () => {
                const target = window.parent.document.getElementById("checklist-export-section");
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "center" });
                }
            });
        }
        </script>
        """,
        height=150,
    )


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
