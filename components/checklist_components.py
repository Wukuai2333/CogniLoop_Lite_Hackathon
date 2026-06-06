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
    st.progress(completed / total if total else 0)
    st.caption(f"Overall progress: {completed} / {total} optional checks completed")

    left, right = st.columns([0.72, 0.28])
    with left:
        st.caption(f"{stage['title']} · Step {step_index + 1} of {len(stage['items'])}")
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

        nav1, nav2, nav3 = st.columns([1, 1, 2])
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
        with nav3:
            render_autosave_indicator()

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
