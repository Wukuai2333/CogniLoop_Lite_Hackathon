from components.layout import configure_page, render_sidebar
from components.contextual_assistant import (
    capture_selection_request,
    render_contextual_assistant,
    render_selection_capture_banner,
)
from utils.env import load_local_env

from pages import ai_assistant, checklist, conversation_first, customize, docs_navigator, home, tutorial


ROUTES = {
    "home": home.render,
    "tutorial": tutorial.render,
    "docs_navigator": docs_navigator.render,
    "checklist": checklist.render,
    "ai_assistant": ai_assistant.render,
    "conversation_first": conversation_first.render,
    "customize": customize.render,
}


def main() -> None:
    configure_page()
    load_local_env()
    page_key = render_sidebar()
    capture_selection_request(page_key)
    render_selection_capture_banner(page_key)
    ROUTES[page_key]()
    render_contextual_assistant(page_key)


if __name__ == "__main__":
    main()
