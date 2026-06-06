import asyncio
import json
import sys

from utils.assistant_runtime import (
    DEMO_DATASET,
    load_assistant_env,
    load_demo_documents,
    normalize_recall_result,
)


async def initialize() -> dict:
    load_assistant_env()
    documents = load_demo_documents()
    if not documents:
        return {"ok": False, "error": "No Markdown documents found in /data."}

    import cognee

    await cognee.add(documents, dataset_name=DEMO_DATASET)
    await cognee.cognify(datasets=[DEMO_DATASET])
    return {
        "ok": True,
        "message": f"Initialized {len(documents)} local Markdown document(s) in dataset `{DEMO_DATASET}`.",
    }


async def ask(question: str) -> dict:
    load_assistant_env()
    import cognee

    results = await cognee.recall(question, datasets=[DEMO_DATASET], top_k=5)
    return {"ok": True, "results": [normalize_recall_result(result) for result in results]}


async def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if command == "init":
            result = await initialize()
        elif command == "ask":
            payload = json.loads(sys.stdin.read() or "{}")
            result = await ask(payload.get("question", ""))
        else:
            result = {"ok": False, "error": f"Unknown command: {command}"}
    except Exception as exc:
        result = {"ok": False, "error": str(exc)}

    print(json.dumps(result))


if __name__ == "__main__":
    asyncio.run(main())
