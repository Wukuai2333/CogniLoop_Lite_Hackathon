import html

import streamlit as st

from components.layout import page_header
from utils.assistant_runtime import (
    cognee_status,
    demo_document_inventory,
    key_status,
    load_demo_documents,
    normalize_recall_result,
    recall_answer,
    remember_demo_documents,
    reset_local_cognee_storage,
    user_friendly_error,
)


def render_optional_notice() -> None:
    st.info(
        "This assistant is a lightweight local test helper. You can skip it completely and still finish the workflow."
    )
    st.caption(
        "Safety boundary: this page does not collect API keys and has no password input. "
        "It only reads a key from your local `.env` or existing environment variables."
    )


def render_connection_status(message: str) -> None:
    st.markdown(
        f"""
        <style>
        .assistant-connection {{
            border: 1px solid rgba(139, 148, 158, 0.32);
            border-radius: 6px;
            padding: 0.75rem 0.9rem;
            margin: 0.5rem 0 1rem 0;
            background: rgba(139, 148, 158, 0.08);
            color: #c9d1d9;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .assistant-connection-dots span {{
            display: inline-block;
            animation: assistantDotBounce 1s infinite ease-in-out;
            font-weight: 700;
        }}
        .assistant-connection-dots span:nth-child(2) {{
            animation-delay: 0.14s;
        }}
        .assistant-connection-dots span:nth-child(3) {{
            animation-delay: 0.28s;
        }}
        @keyframes assistantDotBounce {{
            0%, 80%, 100% {{ transform: translateY(0); opacity: 0.45; }}
            40% {{ transform: translateY(-0.28rem); opacity: 1; }}
        }}
        </style>
        <div class="assistant-connection">
            <div>{message}</div>
            <div class="assistant-connection-dots"><span>.</span><span>.</span><span>.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_action_styles() -> None:
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            min-height: 3rem;
            font-weight: 700;
            border-width: 1px;
        }
        div[data-testid="stButton"] > button[kind="primary"] {
            background: #238636;
            border-color: #2ea043;
            color: #ffffff;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background: #2ea043;
            border-color: #3fb950;
            color: #ffffff;
        }
        div[data-testid="stTextArea"] textarea {
            border: 1px solid rgba(46, 160, 67, 0.58);
            border-radius: 8px;
            font-size: 1rem;
        }
        .assistant-action-hint {
            border-left: 4px solid #2ea043;
            background: rgba(46, 160, 67, 0.12);
            padding: 0.85rem 1rem;
            border-radius: 6px;
            margin: 0.7rem 0 1rem 0;
        }
        .assistant-answer {
            font-size: 1.2rem;
            line-height: 1.72;
            padding: 1rem 1.05rem;
            margin: 0.75rem 0 1rem 0;
            border: 1px solid rgba(46, 160, 67, 0.35);
            border-radius: 8px;
            background: rgba(46, 160, 67, 0.08);
        }
        .assistant-meta-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.65rem;
            margin: 0.6rem 0 0.7rem 0;
        }
        .assistant-meta-card {
            border: 1px solid rgba(139, 148, 158, 0.22);
            border-radius: 6px;
            padding: 0.55rem 0.65rem;
            background: rgba(139, 148, 158, 0.06);
            min-width: 0;
        }
        .assistant-meta-label {
            color: #8b949e;
            font-size: 0.72rem;
            margin-bottom: 0.22rem;
        }
        .assistant-meta-value {
            color: #c9d1d9;
            font-size: 0.86rem;
            line-height: 1.25;
            overflow-wrap: anywhere;
        }
        .assistant-score-note {
            color: #8b949e;
            font-size: 0.78rem;
            margin: 0.15rem 0 0.5rem 0;
        }
        @media (max-width: 900px) {
            .assistant-meta-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_runtime_overview() -> None:
    with st.container(border=True):
        st.markdown("#### Runtime Flow")
        st.markdown(
            "1. Read local `.env` for provider credentials.\n"
            "2. Load Markdown files from `data`.\n"
            "3. Build or query local Cognee memory.\n"
            "4. Call the configured provider only when Cognee needs model output."
        )
        st.caption("No key is typed into this page. The assistant only reads local environment configuration.")


def render() -> None:
    page_header("AI Assistant", "Local `.env`-only Cognee test helper for the demo dataset.")
    render_action_styles()
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

    with st.expander("Official Cognee setup notebook", expanded=False):
        st.write(
            "Cognee provides an official Colab setup notebook. Open it when you want a guided notebook-style setup. "
            "CogniLoop keeps the link here instead of embedding the notebook because Colab is best opened directly."
        )
        st.link_button(
            "Open Cognee Colab Setup",
            "https://colab.research.google.com/drive/1HRrzIvzcbwrESVfX76wJLKmtIg00SUga?usp=sharing",
        )

    disabled = not key_ok or not cognee_ok
    documents = load_demo_documents()
    render_runtime_overview()

    st.subheader("1. Initialize local demo documents")
    st.write("This loads Markdown files from the `data` folder into a small project-local Cognee demo dataset.")
    st.caption("Under the hood: Cognee runs `add()` and `cognify()` first. After that, `recall()` can answer questions.")
    st.markdown(
        "<div class='assistant-action-hint'><strong>Start here:</strong> initialize the local dataset before asking questions.</div>",
        unsafe_allow_html=True,
    )
    with st.expander(f"Dataset preview ({len(documents)} Markdown files)", expanded=False):
        if documents:
            st.write("The current sample dataset includes local Cognee summaries plus a small business crisis mini dataset.")
            st.caption("The `cognee_*.md` files are our short local summaries/placeholders, not official Cognee docs.")
            st.table(demo_document_inventory())
        else:
            st.warning("No Markdown documents found in `/data`.")
    st.caption(
        "Local storage note: Cognee's local demo storage is kept in project folders: `.cognee_system`, "
        "`.data_storage`, and `.cognee_cache`. This makes the demo easy to inspect or reset."
    )
    if st.button("Initialize /data documents", disabled=disabled, type="primary", use_container_width=False):
        with st.status("Connecting local Cognee runtime...", expanded=True) as status:
            try:
                render_connection_status("Reading `.env`, loading `data`, and building local Cognee memory")
                st.write("Loading Markdown files from `data`.")
                st.write("Running Cognee `add()` and `cognify()`.")
                st.success(remember_demo_documents())
                status.update(label="Local Cognee memory initialized.", state="complete")
            except Exception as exc:
                st.error(f"Cognee initialization failed: {user_friendly_error(exc)}")
                status.update(label="Cognee initialization failed.", state="error")

    with st.expander("Troubleshooting local Cognee storage", expanded=False):
        st.write(
            "If you see a database lock error, reset the project-local Cognee store. "
            "This deletes the local demo memory only; it does not touch `.env` or your source files. "
            "If the lock persists after reset, restart Streamlit so Windows releases the local graph database file."
        )
        if st.button("Reset local Cognee storage"):
            try:
                st.success(reset_local_cognee_storage())
            except Exception as exc:
                st.error(f"Reset failed: {exc}")

    st.subheader("2. Ask the local test assistant")
    st.caption("If this is a fresh run or you just reset storage, initialize `/data` first before asking.")
    question = st.text_area(
        "Question",
        value="What is Cognee and how does it help hackathon participants?",
        height=100,
    )
    if st.button("Ask", disabled=disabled or not question.strip(), type="primary"):
        with st.status("Querying local Cognee memory...", expanded=True) as status:
            try:
                render_connection_status("Retrieving context locally, then using the provider configured through `.env`")
                st.write("Searching the project-local Cognee dataset.")
                st.write("Calling the configured provider only if Cognee needs model output.")
                results = recall_answer(question.strip())
                st.markdown("### Result")
                if not results:
                    st.warning("No answer returned.")
                for index, result in enumerate(results, start=1):
                    normalized = normalize_recall_result(result)
                    with st.container(border=True):
                        st.markdown(f"#### Answer {index}")
                        answer_text = html.escape(normalized["answer"] or "No answer text returned.")
                        st.markdown(
                            f"<div class='assistant-answer'>{answer_text}</div>",
                            unsafe_allow_html=True,
                        )

                        source = html.escape(str(normalized["source"] or "n/a"))
                        search_type = html.escape(str(normalized["search_type"] or "n/a"))
                        dataset_name = html.escape(str(normalized["dataset_name"] or "n/a"))
                        score = html.escape(str(normalized["score"] if normalized["score"] is not None else "n/a"))
                        st.markdown(
                            f"""
                            <div class="assistant-meta-grid">
                                <div class="assistant-meta-card">
                                    <div class="assistant-meta-label">Source</div>
                                    <div class="assistant-meta-value">{source}</div>
                                </div>
                                <div class="assistant-meta-card">
                                    <div class="assistant-meta-label">Search type</div>
                                    <div class="assistant-meta-value">{search_type}</div>
                                </div>
                                <div class="assistant-meta-card">
                                    <div class="assistant-meta-label">Dataset</div>
                                    <div class="assistant-meta-value">{dataset_name}</div>
                                </div>
                                <div class="assistant-meta-card">
                                    <div class="assistant-meta-label">Cognee score</div>
                                    <div class="assistant-meta-value">{score}</div>
                                </div>
                            </div>
                            <div class="assistant-score-note">
                                Cognee score is an optional confidence or relevance value returned by some search modes.
                                Graph completion often returns <code>n/a</code>, so it is diagnostic metadata, not a user grade.
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        with st.expander("Raw result"):
                            st.json(normalized["raw"])
                status.update(label="Answer retrieved.", state="complete")
            except Exception as exc:
                st.error(f"Cognee recall failed: {user_friendly_error(exc)}")
                status.update(label="Cognee recall failed.", state="error")
