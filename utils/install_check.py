import importlib.util
import platform
import sys


def python_version_status() -> tuple[bool, str]:
    version = sys.version_info
    supported = (3, 10) <= (version.major, version.minor) <= (3, 14)
    label = platform.python_version()
    if supported:
        return True, f"Python {label} is in the Cognee-supported range."
    return False, f"Python {label} is outside the Cognee-supported range of 3.10-3.14."


def cognee_import_status() -> tuple[bool, str]:
    spec = importlib.util.find_spec("cognee")
    if spec is None:
        return False, "Cognee is not installed in the Python environment running this app."
    return True, "Cognee is importable in the Python environment running this app."
