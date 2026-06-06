import json
from pathlib import Path
import time
from typing import Any


DOCS_PROGRESS_FILE = Path(".cogniloop_docs_progress.json")

DEFAULT_DOCS_PROGRESS = {
    "selected_route": "fast_start",
    "current_steps": {},
    "completed": {},
    "notes": {},
    "bookmarks": [],
    "saved_at": None,
}


def load_docs_progress() -> dict[str, Any]:
    if not DOCS_PROGRESS_FILE.exists():
        return DEFAULT_DOCS_PROGRESS.copy()

    try:
        data = json.loads(DOCS_PROGRESS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_DOCS_PROGRESS.copy()

    progress = DEFAULT_DOCS_PROGRESS.copy()
    progress.update({key: data.get(key, value) for key, value in DEFAULT_DOCS_PROGRESS.items()})
    return progress


def save_docs_progress(progress: dict[str, Any]) -> None:
    progress["saved_at"] = time.time()
    DOCS_PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def docs_step_key(route_id: str, step_index: int) -> str:
    return f"{route_id}:{step_index}"
