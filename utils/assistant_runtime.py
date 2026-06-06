from pathlib import Path
import os
from typing import Any

from dotenv import load_dotenv


DEMO_DATASET = "cogniloop_lite_demo"


def load_assistant_env() -> None:
    load_dotenv(Path(".env"))
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if api_key:
        os.environ.setdefault("LLM_API_KEY", api_key)
        os.environ.setdefault("OPENAI_API_KEY", api_key)
    os.environ.setdefault("ENABLE_BACKEND_ACCESS_CONTROL", "false")


def key_status() -> tuple[bool, str]:
    load_assistant_env()
    if os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"):
        return True, "API key found in local .env or environment variables."
    return False, "No API key found. Add LLM_API_KEY or OPENAI_API_KEY to local .env."


def cognee_status() -> tuple[bool, str]:
    try:
        import cognee  # noqa: F401
    except Exception as exc:
        return False, f"Cognee import failed: {exc}"
    return True, "Cognee is installed and importable."


def load_demo_documents(data_dir: Path = Path("data")) -> list[str]:
    documents: list[str] = []
    for path in sorted(data_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(f"# Source: {path.name}\n\n{text}")
    return documents


def remember_demo_documents() -> str:
    load_assistant_env()
    documents = load_demo_documents()
    if not documents:
        return "No Markdown documents found in /data."

    import cognee

    cognee.remember(documents, dataset_name=DEMO_DATASET)
    return f"Remembered {len(documents)} local Markdown document(s) in dataset `{DEMO_DATASET}`."


def recall_answer(question: str) -> list[Any]:
    load_assistant_env()
    import cognee

    return cognee.recall(question, datasets=[DEMO_DATASET], top_k=5)


def format_recall_results(results: list[Any]) -> str:
    if not results:
        return "No answer returned."

    chunks = []
    for index, result in enumerate(results, start=1):
        if hasattr(result, "model_dump"):
            chunks.append(f"Result {index}\n{result.model_dump()}")
        else:
            chunks.append(f"Result {index}\n{result}")
    return "\n\n".join(chunks)
