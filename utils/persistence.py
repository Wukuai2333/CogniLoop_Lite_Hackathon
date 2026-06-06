import json
from pathlib import Path
import time
from typing import Any


PROGRESS_FILE = Path(".cogniloop_progress.json")


DEFAULT_PROGRESS = {
    "current_stage": 0,
    "current_step": 0,
    "checks": {},
    "notes": {},
    "bookmarks": [],
    "saved_at": None,
}


def load_progress() -> dict[str, Any]:
    if not PROGRESS_FILE.exists():
        return DEFAULT_PROGRESS.copy()

    try:
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_PROGRESS.copy()

    progress = DEFAULT_PROGRESS.copy()
    progress.update({key: data.get(key, value) for key, value in DEFAULT_PROGRESS.items()})
    return progress


def save_progress(progress: dict[str, Any]) -> None:
    progress["saved_at"] = time.time()
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def step_key(stage_id: str, index: int) -> str:
    return f"{stage_id}:{index}"
