from components.layout import configure_page, render_sidebar
from utils.env import load_local_env

from pages import checklist, conversation_first, customize, docs_navigator, home, tutorial


ROUTES = {
    "home": home.render,
    "tutorial": tutorial.render,
    "docs_navigator": docs_navigator.render,
    "checklist": checklist.render,
    "conversation_first": conversation_first.render,
    "customize": customize.render,
}


def main() -> None:
    configure_page()
    load_local_env()
    page_key = render_sidebar()
    ROUTES[page_key]()


if __name__ == "__main__":
    main()
