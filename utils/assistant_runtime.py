from pathlib import Path
import asyncio
import inspect
import json
import os
import shutil
import subprocess
import sys
from typing import Any

from dotenv import load_dotenv


DEMO_DATASET = "cogniloop_lite_demo"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
COGNEE_SYSTEM_DIR = PROJECT_ROOT / ".cognee_system"
COGNEE_DATA_DIR = PROJECT_ROOT / ".data_storage"
COGNEE_CACHE_DIR = PROJECT_ROOT / ".cognee_cache"


def ensure_cognee_local_dirs() -> None:
    for directory in [
        COGNEE_SYSTEM_DIR,
        COGNEE_SYSTEM_DIR / "databases",
        COGNEE_SYSTEM_DIR / "logs",
        COGNEE_DATA_DIR,
        COGNEE_CACHE_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def reset_local_cognee_storage() -> str:
    for directory in [COGNEE_SYSTEM_DIR, COGNEE_DATA_DIR, COGNEE_CACHE_DIR]:
        if directory.exists():
            shutil.rmtree(directory)
    ensure_cognee_local_dirs()
    return "Local Cognee storage was reset. Initialize /data documents again before asking questions."


def run_maybe_async(value: Any) -> Any:
    if not inspect.isawaitable(value):
        return value

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(value)

    if loop.is_running():
        raise RuntimeError("Cognee returned an async task while an event loop is already running.")
    return loop.run_until_complete(value)


async def initialize_cognee_dataset(documents: list[str]) -> None:
    import cognee

    await cognee.add(documents, dataset_name=DEMO_DATASET)
    await cognee.cognify(datasets=[DEMO_DATASET])


def load_assistant_env() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    ensure_cognee_local_dirs()
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if api_key:
        os.environ.setdefault("LLM_API_KEY", api_key)
        os.environ.setdefault("OPENAI_API_KEY", api_key)
    os.environ.setdefault("ENABLE_BACKEND_ACCESS_CONTROL", "false")
    os.environ["SYSTEM_ROOT_DIRECTORY"] = str(COGNEE_SYSTEM_DIR)
    os.environ["DATA_ROOT_DIRECTORY"] = str(COGNEE_DATA_DIR)
    os.environ["CACHE_ROOT_DIRECTORY"] = str(COGNEE_CACHE_DIR)
    os.environ["COGNEE_LOGS_DIR"] = str(COGNEE_SYSTEM_DIR / "logs")


def key_status() -> tuple[bool, str]:
    load_assistant_env()
    if os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"):
        return True, "API key found in local .env or environment variables."
    return False, "No API key found. Add LLM_API_KEY or OPENAI_API_KEY to local .env."


def cognee_status() -> tuple[bool, str]:
    import importlib.util

    if importlib.util.find_spec("cognee") is None:
        return False, "Cognee is not installed in this environment."
    return True, "Cognee is installed and importable."


def load_demo_documents(data_dir: Path = PROJECT_ROOT / "data") -> list[str]:
    documents: list[str] = []
    preferred_files = [
        "cognee_intro.md",
        "cognee_installation.md",
        "cognee_quickstart.md",
        "business_crisis_sample_dataset.md",
    ]
    paths = [data_dir / name for name in preferred_files if (data_dir / name).exists()]
    for path in paths:
        text = path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(f"# Source: {path.name}\n\n{text}")
    return documents


def demo_document_inventory(data_dir: Path = PROJECT_ROOT / "data") -> list[dict[str, str]]:
    inventory: list[dict[str, str]] = []
    for path in sorted(data_dir.glob("*.md")):
        source_type = "Sample dataset"
        if path.name.startswith("cognee_") or path.name == "sponsor_docs_placeholder.md":
            source_type = "Local summary / placeholder"
        if "public_sources" in path.name:
            source_type = "Public source index"
        inventory.append({"name": path.name, "type": source_type})
    return inventory


def user_friendly_error(exc: Exception) -> str:
    message = str(exc)
    if "Could not set lock" in message or "lock" in message.lower():
        return (
            "Cognee could not lock the local graph database. This usually means a previous run still has the "
            "local store open or the local store needs a reset. Try the reset button below, then remember the "
            "documents again. If it still happens, restart the Streamlit app so Windows releases the database lock."
        )
    if "Recall prerequisites not met" in message or "no database/default user found" in message:
        return (
            "Cognee has not been initialized yet. Run `Initialize /data documents` first. "
            "That step adds the local Markdown files and builds Cognee memory before recall can answer."
        )
    if "bound to a different event loop" in message:
        return (
            "Cognee hit an async event-loop conflict while initializing local memory. "
            "Restart Streamlit, reset local Cognee storage, and initialize again."
        )
    if "Embedding endpoint timed out" in message or "Embedding request timed out" in message:
        return (
            "The embedding step timed out while building local Cognee memory. Check that your provider key is valid, "
            "then try initializing the smaller default dataset again."
        )
    return message


def run_worker(command: str, payload: dict[str, Any] | None = None, timeout: int = 180) -> dict[str, Any]:
    load_assistant_env()
    completed = subprocess.run(
        [sys.executable, "-m", "utils.cognee_worker", command],
        cwd=PROJECT_ROOT,
        input=json.dumps(payload or {}),
        text=True,
        capture_output=True,
        timeout=timeout,
        env=os.environ.copy(),
    )

    output = completed.stdout.strip().splitlines()[-1] if completed.stdout.strip() else "{}"
    try:
        result = json.loads(output)
    except json.JSONDecodeError:
        result = {"ok": False, "error": completed.stderr.strip() or completed.stdout.strip()}

    if completed.returncode != 0 and result.get("ok", True):
        result = {"ok": False, "error": completed.stderr.strip() or "Cognee worker failed."}
    return result


def remember_demo_documents() -> str:
    load_assistant_env()
    documents = load_demo_documents()
    if not documents:
        return "No Markdown documents found in /data."

    result = run_worker("init", timeout=240)
    if not result.get("ok"):
        raise RuntimeError(result.get("error", "Cognee initialization failed."))
    return result.get("message", f"Initialized dataset `{DEMO_DATASET}`.")


def recall_answer(question: str) -> list[Any]:
    result = run_worker("ask", {"question": question}, timeout=120)
    if not result.get("ok"):
        raise RuntimeError(result.get("error", "Cognee recall failed."))
    return result.get("results", [])


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


def normalize_recall_result(result: Any) -> dict[str, Any]:
    if hasattr(result, "model_dump"):
        data = result.model_dump()
    elif isinstance(result, dict):
        data = result
    else:
        data = {"text": str(result)}

    raw = data.get("raw")
    raw_value = raw.get("value") if isinstance(raw, dict) else None
    text = data.get("text") or raw_value or str(result)

    return {
        "answer": text,
        "source": data.get("source"),
        "search_type": data.get("search_type"),
        "dataset_name": data.get("dataset_name"),
        "score": data.get("score"),
        "raw": data,
    }
