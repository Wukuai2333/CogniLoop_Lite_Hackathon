import streamlit as st


PAGES = {
    "Home": "home",
    "Cognee Tutorial": "tutorial",
    "Docs Navigator": "docs_navigator",
    "Checklist": "checklist",
    "AI Assistant": "ai_assistant",
    "Conversation-first Workflow": "conversation_first",
    "Customize Your Own Cognee": "customize",
}


def configure_page() -> None:
    st.set_page_config(
        page_title="CogniLoop Lite",
        page_icon="CL",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_sidebar() -> str:
    st.sidebar.title("CogniLoop Lite")
    st.sidebar.caption("Local-first Cognee onboarding")
    choice = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
    st.sidebar.divider()
    st.sidebar.caption("Static pages work without an API key. Future assistant features use your local `.env`.")
    return PAGES[choice]


def page_header(title: str, subtitle: str | None = None) -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def callout(title: str, body: str, icon: str = "Info") -> None:
    st.info(f"**{title}**\n\n{body}", icon=None)
