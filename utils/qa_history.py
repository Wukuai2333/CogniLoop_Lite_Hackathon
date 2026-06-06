import json
from pathlib import Path
import time
from typing import Any


QA_HISTORY_FILE = Path(".cogniloop_qa_history.json")


def load_qa_history() -> list[dict[str, Any]]:
    if not QA_HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(QA_HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []


def save_qa_history(history: list[dict[str, Any]]) -> None:
    QA_HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")


def add_qa_entry(page: str, question: str, selected_text: str, answer: str, status: str = "ok") -> None:
    history = load_qa_history()
    history.insert(
        0,
        {
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "page": page,
            "question": question,
            "selected_text": selected_text,
            "answer": answer,
            "status": status,
        },
    )
    save_qa_history(history[:100])


def history_markdown(history: list[dict[str, Any]]) -> str:
    lines = ["# CogniLoop Lite Q&A History", ""]
    for entry in history:
        lines.extend(
            [
                f"## {entry['created_at']} - {entry['page']}",
                "",
                f"Question: {entry['question']}",
                "",
                "Selected text:",
                entry.get("selected_text") or "No selected text provided.",
                "",
                "Answer:",
                entry.get("answer") or "No answer recorded.",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"
