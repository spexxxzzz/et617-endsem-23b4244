"""Small allow-listed .env loader; existing process environment wins."""

import os
from pathlib import Path


def load_environment():
    path = Path(".env")
    if not path.exists():
        return
    allowed = {
        "HYDE_API_KEY", "HYDE_BASE_URL", "HYDE_MODEL", "HYDE_VERIFIER_MODEL", "STUDENT_ROLL", "APP_ALLOWED_HOSTS", "APP_PUBLIC_ORIGIN", "SESSION_SECRET", "EQUATION8_STATELESS",
        "GEMINI_API_KEY",
        "GEMINI_MODEL",
        "GEMINI_VERIFIER_MODEL",
        "EQUATION8_DATA_DIR",
    }
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            if key.strip() in allowed:
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
