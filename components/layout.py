import streamlit as st


PAGES = {
    "Home": "home",
    "Cognee Tutorial": "tutorial",
    "Docs Navigator": "docs_navigator",
    "Task Progress Checklist": "checklist",
    "AI Assistant": "ai_assistant",
    "Conversation-first Workflow": "conversation_first",
    "Customize Your Own Cognee": "customize",
}


def render_sidebar_styles() -> None:
    st.sidebar.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(139, 148, 158, 0.18);
        }
        section[data-testid="stSidebar"] h1 {
            font-size: 1.85rem;
            letter-spacing: 0;
            margin-bottom: 0.35rem;
        }
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: #a5a8b0;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0.2rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            border: 1px solid transparent;
            border-radius: 8px;
            padding: 0.58rem 0.7rem;
            margin: 0.08rem 0;
            transition: background 140ms ease, border-color 140ms ease, color 140ms ease;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(46, 160, 67, 0.08);
            border-color: rgba(46, 160, 67, 0.22);
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: rgba(46, 160, 67, 0.15);
            border-color: rgba(46, 160, 67, 0.44);
            box-shadow: inset 3px 0 0 #2ea043;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            display: none;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label p {
            font-weight: 650;
            font-size: 0.98rem;
            line-height: 1.25;
        }
        section[data-testid="stSidebar"] code {
            color: #56d364;
            background: rgba(46, 160, 67, 0.12);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def configure_page() -> None:
    st.set_page_config(
        page_title="CogniLoop Lite",
        page_icon="CL",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_sidebar() -> str:
    render_sidebar_styles()
    st.sidebar.title("CogniLoop Lite")
    st.sidebar.caption("Hosted guide. Local-first demo.")
    labels = list(PAGES.keys())
    requested_page = st.query_params.get("page", "")
    default_key = requested_page if requested_page in PAGES.values() else "home"
    default_label = next(label for label, key in PAGES.items() if key == default_key)
    choice = st.sidebar.radio(
        "Navigate",
        labels,
        index=labels.index(default_label),
        label_visibility="collapsed",
    )
    selected_key = PAGES[choice]
    if st.query_params.get("page") != selected_key:
        st.query_params["page"] = selected_key
    st.sidebar.divider()
    st.sidebar.caption(
        "Public demos ship with `.env.example` only. Clone locally and create `.env` to enable Cognee assistant tests."
    )
    return selected_key


def page_header(title: str, subtitle: str | None = None) -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def callout(title: str, body: str, icon: str = "Info") -> None:
    st.info(f"**{title}**\n\n{body}", icon=None)
