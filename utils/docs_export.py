from content.docs_routes import DOC_ROUTES
from utils.docs_progress import docs_step_key


def route_markdown(route: dict, progress: dict) -> str:
    lines = [
        f"# {route['name']} Route Notes",
        "",
        f"Best for: {route['best_for']}",
        f"Outcome: {route['outcome']}",
        "",
    ]

    for index, step in enumerate(route["steps"], start=1):
        key = docs_step_key(route["id"], index - 1)
        checked = "x" if progress["completed"].get(key) else " "
        note = progress["notes"].get(key, "").strip()
        lines.extend(
            [
                f"## {index}. {step['title']}",
                "",
                f"- [{checked}] Read / applied",
                f"- Official docs: {step['url']}",
                f"- Why it matters: {step['why']}",
                f"- Hackathon use: {step['hackathon_use']}",
                f"- Deliverable: {step['deliverable']}",
                "",
                "Notes:",
                note or "No notes yet.",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def all_routes_markdown(progress: dict) -> str:
    sections = ["# CogniLoop Lite Docs Navigator Notes", ""]
    for route in DOC_ROUTES:
        sections.append(route_markdown(route, progress))
    return "\n\n".join(sections)
