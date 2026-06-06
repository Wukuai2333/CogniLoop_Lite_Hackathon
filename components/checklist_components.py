import streamlit as st

from content.checklist_content import CHECKLIST_STAGES
from utils.export import full_markdown, stage_markdown
from utils.persistence import save_progress, step_key


def render_autosave_indicator() -> None:
    st.markdown(
        """
        <style>
        .autosave-line {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            color: #8b949e;
            font-size: 0.86rem;
            margin-top: 0.25rem;
        }
        .autosave-dot {
            width: 0.55rem;
            height: 0.55rem;
            border-radius: 999px;
            background: #2ea043;
            animation: autosavePulse 1.4s ease-in-out infinite;
        }
        @keyframes autosavePulse {
            0% { opacity: 0.35; transform: scale(0.86); }
            50% { opacity: 1; transform: scale(1); }
            100% { opacity: 0.35; transform: scale(0.86); }
        }
        </style>
        <div class="autosave-line">
            <span class="autosave-dot"></span>
            <span>Auto saved</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def current_bookmark(progress: dict) -> dict:
    stage_index = progress["current_stage"]
    step_index = progress["current_step"]
    stage = CHECKLIST_STAGES[stage_index]
    item = stage["items"][step_index]
    return {
        "stage_index": stage_index,
        "step_index": step_index,
        "stage_id": stage["id"],
        "stage_title": stage["title"],
        "step_title": item["text"],
    }


def bookmark_label(bookmark: dict) -> str:
    return f"Step {bookmark['step_index'] + 1}: {bookmark['step_title']}"


def render_step_context(stage: dict, step_index: int, item: dict) -> None:
    st.markdown(
        f"""
        <div class="step-context">
            <span>{stage['title']}</span>
            <strong>Step {step_index + 1}: {item['text']}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bookmarks(progress: dict) -> None:
    col1, col2 = st.columns([0.18, 0.82])
    with col1:
        if st.button("Add Bookmark", use_container_width=True):
            progress.setdefault("bookmarks", []).append(current_bookmark(progress))
            save_progress(progress)
            st.toast("Bookmark added.")
            st.rerun()
    with col2:
        bookmarks = progress.setdefault("bookmarks", [])
        title = f"Resume Bookmarks ({len(bookmarks)})"
        with st.expander(title, expanded=False):
            if not bookmarks:
                st.caption("No bookmarks yet. Add one from any substep.")
            for stage_index, stage in enumerate(CHECKLIST_STAGES):
                stage_bookmarks = [
                    (index, bookmark)
                    for index, bookmark in enumerate(bookmarks)
                    if bookmark["stage_index"] == stage_index
                ]
                if not stage_bookmarks:
                    continue

                st.markdown(f"**{stage['title']}**")
                for index, bookmark in stage_bookmarks:
                    jump, remove = st.columns([0.84, 0.16])
                    with jump:
                        if st.button(bookmark_label(bookmark), key=f"bookmark_jump::{index}", use_container_width=True):
                            progress["current_stage"] = bookmark["stage_index"]
                            progress["current_step"] = bookmark["step_index"]
                            save_progress(progress)
                            st.rerun()
                    with remove:
                        if st.button("Remove", key=f"bookmark_remove::{index}", use_container_width=True):
                            bookmarks.pop(index)
                            save_progress(progress)
                            st.rerun()


def clamp_position(progress: dict) -> None:
    progress["current_stage"] = max(0, min(progress["current_stage"], len(CHECKLIST_STAGES) - 1))
    stage = CHECKLIST_STAGES[progress["current_stage"]]
    progress["current_step"] = max(0, min(progress["current_step"], len(stage["items"]) - 1))


def total_counts(progress: dict) -> tuple[int, int]:
    total = sum(len(stage["items"]) for stage in CHECKLIST_STAGES)
    completed = sum(1 for value in progress["checks"].values() if value)
    return completed, total


def flat_position(stage_index: int, step_index: int) -> int:
    return sum(len(stage["items"]) for stage in CHECKLIST_STAGES[:stage_index]) + step_index + 1


def move(progress: dict, delta: int) -> None:
    stage_index = progress["current_stage"]
    step_index = progress["current_step"] + delta

    while stage_index >= 0 and stage_index < len(CHECKLIST_STAGES):
        stage_len = len(CHECKLIST_STAGES[stage_index]["items"])
        if 0 <= step_index < stage_len:
            progress["current_stage"] = stage_index
            progress["current_step"] = step_index
            save_progress(progress)
            return
        if step_index >= stage_len:
            stage_index += 1
            step_index = 0
        else:
            stage_index -= 1
            if stage_index >= 0:
                step_index = len(CHECKLIST_STAGES[stage_index]["items"]) - 1


def render_stage_picker(progress: dict) -> None:
    st.subheader("Jump to Stage")
    labels = [stage["title"] for stage in CHECKLIST_STAGES]
    choice = st.selectbox(
        "Stage",
        range(len(labels)),
        format_func=lambda index: labels[index],
        index=progress["current_stage"],
        label_visibility="collapsed",
    )
    if choice != progress["current_stage"]:
        progress["current_stage"] = choice
        progress["current_step"] = 0
        save_progress(progress)
        st.rerun()

    stage = CHECKLIST_STAGES[progress["current_stage"]]
    st.caption(f"{progress['current_step'] + 1} / {len(stage['items'])} in this stage")


def render_reader(progress: dict) -> None:
    clamp_position(progress)
    stage_index = progress["current_stage"]
    step_index = progress["current_step"]
    stage = CHECKLIST_STAGES[stage_index]
    item = stage["items"][step_index]
    key = step_key(stage["id"], step_index)

    completed, total = total_counts(progress)
    st.markdown(
        """
        <style>
        .step-context {
            border: 1px solid rgba(139, 148, 158, 0.32);
            border-left: 4px solid #2f81f7;
            border-radius: 6px;
            padding: 0.7rem 0.85rem;
            margin: 0.6rem 0 1rem 0;
            background: rgba(139, 148, 158, 0.08);
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        .step-context span {
            color: #8b949e;
            font-size: 0.84rem;
        }
        .step-context strong {
            color: inherit;
            font-size: 1rem;
            line-height: 1.35;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    top_left, top_right = st.columns([0.78, 0.22])
    with top_left:
        st.progress(completed / total if total else 0)
        st.caption(f"Overall progress: {completed} / {total} checks completed")
    with top_right:
        render_autosave_indicator()

    render_bookmarks(progress)

    left, right = st.columns([0.72, 0.28])
    with left:
        render_step_context(stage, step_index, item)
        st.header(item["text"])
        st.write(stage["goal"])
        st.info(item["detail"])

        checked = st.checkbox(
            "Mark as done",
            value=bool(progress["checks"].get(key)),
            key=f"reader_check::{key}",
        )
        note = st.text_area(
            item["prompt"],
            value=progress["notes"].get(key, ""),
            height=180,
            key=f"reader_note::{key}",
        )

        progress["checks"][key] = checked
        progress["notes"][key] = note
        save_progress(progress)

        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button("Previous", use_container_width=True, disabled=stage_index == 0 and step_index == 0):
                save_progress(progress)
                move(progress, -1)
                st.rerun()
        with nav2:
            last_step = stage_index == len(CHECKLIST_STAGES) - 1 and step_index == len(stage["items"]) - 1
            if st.button("Next", use_container_width=True, disabled=last_step):
                save_progress(progress)
                move(progress, 1)
                st.rerun()

    with right:
        render_stage_picker(progress)
        st.divider()
        st.subheader("Current Stage Notes")
        st.download_button(
            "Download Stage Markdown",
            data=stage_markdown(stage_index, progress),
            file_name=f"{stage['id']}_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.download_button(
            "Download Full Progress",
            data=full_markdown(progress),
            file_name="cogniloop_progress_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.divider()
        st.caption(f"Reading position: {flat_position(stage_index, step_index)} / {total}")
