import streamlit as st
import streamlit.components.v1 as components

from components.layout import page_header
from content.docs_catalog import OFFICIAL_COLAB_SETUP, OFFICIAL_DOC_SECTIONS
from content.docs_routes import DOC_ROUTES
from utils.docs_export import all_routes_markdown, route_markdown
from utils.docs_progress import docs_step_key, load_docs_progress, save_docs_progress


def route_by_id(route_id: str) -> dict:
    return next((route for route in DOC_ROUTES if route["id"] == route_id), DOC_ROUTES[0])


def completed_count(route: dict, progress: dict) -> int:
    return sum(
        1
        for index, _ in enumerate(route["steps"])
        if progress["completed"].get(docs_step_key(route["id"], index))
    )


def render_autosave() -> None:
    st.markdown(
        """
        <style>
        .docs-autosave {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            color: #8b949e;
            font-size: 0.86rem;
            justify-content: flex-end;
        }
        .docs-autosave-dot {
            width: 0.55rem;
            height: 0.55rem;
            border-radius: 999px;
            background: #2ea043;
            animation: docsAutosavePulse 1.4s ease-in-out infinite;
        }
        .docs-step-context {
            border: 1px solid rgba(139, 148, 158, 0.32);
            border-left: 4px solid #2f81f7;
            border-radius: 6px;
            padding: 0.75rem 0.9rem;
            margin: 0.75rem 0 1rem 0;
            background: rgba(139, 148, 158, 0.08);
        }
        .docs-step-context span {
            display: block;
            color: #8b949e;
            font-size: 0.84rem;
            margin-bottom: 0.22rem;
        }
        .docs-step-context strong {
            font-size: 1rem;
            line-height: 1.35;
        }
        @keyframes docsAutosavePulse {
            0% { opacity: 0.35; transform: scale(0.86); }
            50% { opacity: 1; transform: scale(1); }
            100% { opacity: 0.35; transform: scale(0.86); }
        }
        </style>
        <div class="docs-autosave">
            <span class="docs-autosave-dot"></span>
            <span>Auto saved</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_export_focus(anchor_id: str, should_focus: bool) -> None:
    st.markdown(
        f"""
        <style>
        #{anchor_id} {{
            scroll-margin-top: 5rem;
        }}
        .export-focus-card {{
            border: 1px solid rgba(46, 160, 67, 0.42);
            border-radius: 8px;
            padding: 0.75rem;
            background: rgba(46, 160, 67, 0.07);
        }}
        .export-focus-card.is-active {{
            animation: exportFocusPulse 2.2s ease-in-out 1;
        }}
        @keyframes exportFocusPulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(46, 160, 67, 0.62); }}
            50% {{ box-shadow: 0 0 0 8px rgba(46, 160, 67, 0.14); }}
            100% {{ box-shadow: 0 0 0 0 rgba(46, 160, 67, 0); }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    if should_focus:
        components.html(
            f"""
            <script>
            const target = window.parent.document.getElementById("{anchor_id}");
            if (target) {{
                setTimeout(() => target.scrollIntoView({{ behavior: "smooth", block: "center" }}), 120);
            }}
            </script>
            """,
            height=0,
        )


def render_agent_alignment_hint(key: str, show_focus_button: bool = True) -> None:
    st.info(
        "Hint: keep your agents on the same page as you. Export your current progress as Markdown, including notes "
        "from each step, so you can give agents clearer structure, more token-efficient context, and less chance of "
        "losing the thread during implementation."
    )
    if show_focus_button and st.button("Show download buttons", key=key):
        st.session_state["docs_focus_export"] = True
        st.rerun()


def render_route_selector(progress: dict) -> dict:
    route_names = [route["name"] for route in DOC_ROUTES]
    current_route = route_by_id(progress["selected_route"])
    selected_name = st.segmented_control("Route", route_names, default=current_route["name"])
    selected_route = next(route for route in DOC_ROUTES if route["name"] == selected_name)

    if selected_route["id"] != progress["selected_route"]:
        progress["selected_route"] = selected_route["id"]
        progress["current_steps"].setdefault(selected_route["id"], 0)
        save_docs_progress(progress)
        st.rerun()

    return selected_route


def render_context(route: dict, step_index: int, step: dict) -> None:
    st.markdown(
        f"""
        <div class="docs-step-context">
            <span>{route['name']} Route - Step {step_index + 1} of {len(route['steps'])}</span>
            <strong>{step['title']}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_local_runbook(step: dict) -> None:
    local_steps = step.get("local_steps", [])
    verify_items = step.get("verify", [])
    if not local_steps and not verify_items:
        return

    st.markdown("#### Run Locally")
    st.caption(
        "Use these commands in your own terminal, then come back here to check off results and save notes."
    )
    for item in local_steps:
        st.markdown(f"**{item['title']}**")
        st.code(item["code"], language=item.get("language", "bash"))

    if verify_items:
        st.markdown("#### What to Verify")
        for item in verify_items:
            st.markdown(f"- {item}")


def current_bookmark(route: dict, step_index: int) -> dict:
    step = route["steps"][step_index]
    return {
        "route_id": route["id"],
        "route_name": route["name"],
        "step_index": step_index,
        "step_title": step["title"],
    }


def render_bookmarks(progress: dict) -> None:
    add_col, list_col = st.columns([0.18, 0.82])
    route = route_by_id(progress["selected_route"])
    step_index = progress["current_steps"].get(route["id"], 0)

    with add_col:
        if st.button("Add Bookmark", use_container_width=True):
            progress.setdefault("bookmarks", []).append(current_bookmark(route, step_index))
            save_docs_progress(progress)
            st.toast("Bookmark added.")
            st.rerun()

    with list_col:
        bookmarks = progress.setdefault("bookmarks", [])
        with st.expander(f"Docs Bookmarks ({len(bookmarks)})", expanded=False):
            if not bookmarks:
                st.caption("No docs bookmarks yet.")

            for grouped_route in DOC_ROUTES:
                route_bookmarks = [
                    (index, bookmark)
                    for index, bookmark in enumerate(bookmarks)
                    if bookmark["route_id"] == grouped_route["id"]
                ]
                if not route_bookmarks:
                    continue

                st.markdown(f"**{grouped_route['name']}**")
                for index, bookmark in route_bookmarks:
                    jump, remove = st.columns([0.84, 0.16])
                    label = f"Step {bookmark['step_index'] + 1}: {bookmark['step_title']}"
                    with jump:
                        if st.button(label, key=f"docs_bookmark_jump::{index}", use_container_width=True):
                            progress["selected_route"] = bookmark["route_id"]
                            progress["current_steps"][bookmark["route_id"]] = bookmark["step_index"]
                            save_docs_progress(progress)
                            st.rerun()
                    with remove:
                        if st.button("Remove", key=f"docs_bookmark_remove::{index}", use_container_width=True):
                            bookmarks.pop(index)
                            save_docs_progress(progress)
                            st.rerun()


def move_step(progress: dict, route: dict, delta: int) -> None:
    current = progress["current_steps"].get(route["id"], 0)
    next_step = max(0, min(current + delta, len(route["steps"]) - 1))
    progress["current_steps"][route["id"]] = next_step
    save_docs_progress(progress)


def render_step(route: dict, progress: dict) -> None:
    progress["current_steps"].setdefault(route["id"], 0)
    step_index = max(0, min(progress["current_steps"][route["id"]], len(route["steps"]) - 1))
    progress["current_steps"][route["id"]] = step_index
    step = route["steps"][step_index]
    key = docs_step_key(route["id"], step_index)

    done = completed_count(route, progress)
    top_left, top_right = st.columns([0.78, 0.22])
    with top_left:
        st.progress(done / len(route["steps"]))
        st.caption(f"Route progress: {done} / {len(route['steps'])} steps completed")
    with top_right:
        render_autosave()

    render_bookmarks(progress)

    left, right = st.columns([0.7, 0.3])
    with left:
        render_context(route, step_index, step)
        st.header(step["title"])
        st.write(step["why"])
        if step.get("beginner_tip"):
            st.warning(f"Beginner tip: {step['beginner_tip']}")
        st.info(f"Why this matters for hackathon: {step['hackathon_use']}")
        st.success(f"Deliverable: {step['deliverable']}")
        st.link_button("Open Official Docs", step["url"])

        render_local_runbook(step)

        if step.get("checks"):
            st.markdown("#### Quick Checks")
            for check in step["checks"]:
                st.checkbox(check, key=f"docs_quick_check::{key}::{check}")

        if step.get("questions"):
            st.markdown("#### Questions to Ask Yourself")
            for question in step["questions"]:
                st.markdown(f"- {question}")

        progress["completed"][key] = st.checkbox(
            "Mark as done",
            value=bool(progress["completed"].get(key)),
            key=f"docs_done::{key}",
        )
        progress["notes"][key] = st.text_area(
            step["note_prompt"],
            value=progress["notes"].get(key, ""),
            height=180,
            key=f"docs_note::{key}",
        )
        save_docs_progress(progress)

        prev_col, next_col = st.columns(2)
        with prev_col:
            if st.button("Previous", disabled=step_index == 0, use_container_width=True):
                move_step(progress, route, -1)
                st.rerun()
        with next_col:
            if st.button("Next", disabled=step_index == len(route["steps"]) - 1, use_container_width=True):
                move_step(progress, route, 1)
                st.rerun()

    with right:
        st.subheader("Route Map")
        for index, item in enumerate(route["steps"]):
            marker = "Done" if progress["completed"].get(docs_step_key(route["id"], index)) else "Open"
            if st.button(f"{index + 1}. {item['title']} - {marker}", key=f"route_step::{route['id']}::{index}", use_container_width=True):
                progress["current_steps"][route["id"]] = index
                save_docs_progress(progress)
                st.rerun()

        st.divider()
        st.subheader("Official Docs Map")
        for section in OFFICIAL_DOC_SECTIONS:
            with st.expander(section["section"], expanded=False):
                st.caption(section["goal"])
                for label, url in section["pages"]:
                    st.link_button(label, url, use_container_width=True)

        st.divider()
        st.subheader("Export")
        should_focus = bool(st.session_state.pop("docs_focus_export", False))
        render_export_focus("docs-export-section", should_focus)
        active_class = " is-active" if should_focus else ""
        st.markdown(
            f"<div id='docs-export-section' class='export-focus-card{active_class}'>",
            unsafe_allow_html=True,
        )
        render_agent_alignment_hint("docs_export_focus_inside", show_focus_button=False)
        st.caption("Use these two download buttons to package your current route notes or all route notes for your agent.")
        st.download_button(
            "Download This Route",
            data=route_markdown(route, progress),
            file_name=f"{route['id']}_docs_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.download_button(
            "Download All Routes",
            data=all_routes_markdown(progress),
            file_name="cogniloop_docs_navigator_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render() -> None:
    page_header(
        "Cognee Docs Navigator",
        "Turn official Cognee documentation into hackathon-ready learning routes.",
    )

    if "docs_progress" not in st.session_state:
        st.session_state.docs_progress = load_docs_progress()

    progress = st.session_state.docs_progress

    st.write(
        "Cognee's official documentation remains the source of truth. This page adds a companion layer: "
        "route selection, task framing, notes, bookmarks, and exportable project context."
    )
    top_a, top_b = st.columns([0.68, 0.32])
    with top_a:
        st.caption("Docs index for agents and LLM tools: https://docs.cognee.ai/llms.txt")
    with top_b:
        st.link_button(OFFICIAL_COLAB_SETUP["title"], OFFICIAL_COLAB_SETUP["url"], use_container_width=True)
    st.caption(OFFICIAL_COLAB_SETUP["description"])
    render_agent_alignment_hint("docs_export_focus_top")

    route = render_route_selector(progress)
    st.caption(f"Best for: {route['best_for']}")
    st.caption(f"Expected outcome: {route['outcome']}")

    render_step(route, progress)

    st.divider()
    st.info(
        "Future BYOK idea: generate a project-specific implementation prompt from route notes, checklist notes, "
        "and bookmarks. This static version does not call any API."
    )
