from content.checklist_content import CHECKLIST_STAGES
from utils.persistence import step_key


def stage_markdown(stage_index: int, progress: dict) -> str:
    stage = CHECKLIST_STAGES[stage_index]
    lines = [
        f"# {stage['title']}",
        "",
        f"Goal: {stage['goal']}",
        "",
    ]

    for index, item in enumerate(stage["items"]):
        key = step_key(stage["id"], index)
        checked = "x" if progress["checks"].get(key) else " "
        note = progress["notes"].get(key, "").strip()
        lines.extend(
            [
                f"- [{checked}] {item['text']}",
                f"  - Detail: {item['detail']}",
                f"  - Notes: {note or 'No notes yet.'}",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def full_markdown(progress: dict) -> str:
    sections = ["# CogniLoop Lite Progress Notes", ""]
    sections.extend(stage_markdown(index, progress) for index, _ in enumerate(CHECKLIST_STAGES))
    return "\n\n".join(sections)
