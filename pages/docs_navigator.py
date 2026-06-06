import streamlit as st

from components.layout import page_header
from content.docs_routes import DOC_ROUTES


def render_route(route: dict) -> None:
    st.subheader(route["name"])
    st.write(route["best_for"])
    st.caption(f"Outcome: {route['outcome']}")

    for index, step in enumerate(route["steps"], start=1):
        with st.container(border=True):
            st.markdown(f"**{index}. {step['title']}**")
            st.write(step["why"])
            st.caption(f"Deliverable: {step['deliverable']}")
            st.link_button("Open Official Docs", step["url"], use_container_width=False)


def render() -> None:
    page_header(
        "Cognee Docs Navigator",
        "Turn official Cognee documentation into hackathon-ready learning routes.",
    )

    st.write(
        "Cognee's official documentation is the source of truth. This navigator adds a hackathon layer: "
        "what to read, why it matters, and what artifact your team should produce after each step."
    )

    route_names = [route["name"] for route in DOC_ROUTES]
    selected = st.segmented_control("Route", route_names, default=route_names[0])
    route = next(route for route in DOC_ROUTES if route["name"] == selected)

    render_route(route)

    st.divider()
    st.info(
        "Future BYOK idea: combine selected route, checklist notes, and bookmarks into a project-specific prompt. "
        "For now, this page stays static and safe without an API key."
    )
