from pathlib import Path

from dotenv import load_dotenv
import os


def load_local_env() -> None:
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)


def has_api_key() -> bool:
    return bool(os.getenv("LLM_API_KEY"))
