"""Small, dependency-free configuration helpers for the examples."""

from __future__ import annotations

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def load_environment(path: Path | None = None) -> None:
    """Load simple KEY=value entries without replacing shell environment values.

    Supports blank lines, comments, optional ``export`` and quoted values.
    Variable interpolation and shell execution are intentionally unsupported.
    """
    path = path or PROJECT_ROOT / ".env"
    if path.is_file():
        for number, raw_line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].strip()
            key, separator, value = line.partition("=")
            key = key.strip()
            if not separator or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                raise ValueError(f"Invalid environment entry at line {number} of {path.name}")
            value = value.strip()
            if value.startswith(("'", '"')):
                quote = value[0]
                if len(value) < 2 or value[-1] != quote:
                    raise ValueError(f"Unclosed quoted value at line {number} of {path.name}")
                value = value[1:-1]
            else:
                value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
            os.environ.setdefault(key, value)
    key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if key:
        os.environ.setdefault("DASHSCOPE_API_KEY", key)
        os.environ.setdefault("OPENAI_API_KEY", key)
    os.environ.setdefault("OPENAI_BASE_URL", DEFAULT_BASE_URL)


def get_api_key() -> str:
    load_environment()
    key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    if not key.strip() or key.strip().lower() in {"your-api-key", "your_api_key", "replace-me"}:
        raise ValueError("Set DASHSCOPE_API_KEY in .env or your shell before running this example.")
    return key


def get_chat_model_name(default: str = "qwen3-max") -> str:
    return os.environ.get("DASHSCOPE_MODEL") or default


def mysql_settings() -> dict:
    load_environment()
    names = {"username": "MYSQL_USER", "password": "MYSQL_PASSWORD", "database": "MYSQL_DATABASE"}
    missing = [env for env in names.values() if not os.environ.get(env)]
    if missing:
        raise ValueError("Missing database configuration: " + ", ".join(missing))
    try:
        port = int(os.environ.get("MYSQL_PORT", "3306"))
    except ValueError as error:
        raise ValueError("MYSQL_PORT must be an integer.") from error
    if not 1 <= port <= 65535:
        raise ValueError("MYSQL_PORT must be between 1 and 65535.")
    return {"host": os.environ.get("MYSQL_HOST") or "127.0.0.1", "port": port,
            **{field: os.environ[env] for field, env in names.items()}}
