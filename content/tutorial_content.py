TROUBLESHOOTING_ROWS = [
    ("python not found", "Python is not installed or not in PATH", "Install Python 3.10+ and enable Add to PATH."),
    ("uv not recognized", "uv is not installed or the terminal was not restarted", "Run `pip install uv` and reopen the terminal."),
    ("venv activation blocked", "PowerShell execution policy issue", "Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`."),
    ("No module named cognee", "Cognee installed outside the active environment", "Activate `.venv`, then reinstall Cognee."),
    ("API key missing", ".env is missing or the variable name is wrong", "Create `.env` and set `LLM_API_KEY`."),
    ("quota / billing error", "API key has no available quota", "Check billing or use no-key mode."),
]


WINDOWS_INSTALL = """mkdir cogniloop-lite
cd cogniloop-lite

pip install uv
uv venv
.venv\\Scripts\\Activate.ps1

uv pip install cognee"""


POSIX_INSTALL = """mkdir cogniloop-lite
cd cogniloop-lite

pip install uv
uv venv
source .venv/bin/activate

uv pip install cognee"""
