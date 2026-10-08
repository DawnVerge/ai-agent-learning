"""Offline repository checks; never import or execute teaching scripts."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

from .config import PROJECT_ROOT


def check_repository(root: Path = PROJECT_ROOT) -> list[str]:
    errors = []
    ignored = {".git", ".venv", "venv", "__pycache__", ".cache", "build", "dist"}
    for path in root.rglob("*.py"):
        relative = path.relative_to(root)
        if any(part in ignored or part.endswith(".egg-info") for part in relative.parts):
            continue
        source = path.read_text(encoding="utf-8-sig")
        try:
            tree = ast.parse(source, filename=str(relative))
        except SyntaxError as error:
            errors.append(f"{relative}:{error.lineno}: {error.msg}")
            continue
        if relative.parts[0] in {"lessons", "projects"}:
            if re.search(r"[A-Za-z]:[\\/](?:python|Users|Code)[\\/]", source, re.I):
                errors.append(f"{relative}: machine-specific absolute path")
            if re.search(r"sk-[A-Za-z0-9_-]{16,}", source):
                errors.append(f"{relative}: possible API secret")
            for node in ast.walk(tree):
                if isinstance(node, ast.keyword) and node.arg in {"api_key", "password"}:
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str) and node.value.value:
                        errors.append(f"{relative}:{node.lineno}: hardcoded credential argument")
    catalog_path = root / "ai_learning" / "catalog.json"
    if not catalog_path.is_file():
        return errors + ["ai_learning/catalog.json is missing"]
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    seen = set()
    for item in catalog:
        identifier = item["id"]
        if identifier in seen:
            errors.append(f"Duplicate example id: {identifier}")
        seen.add(identifier)
        for field in ("path", "workdir"):
            path = (root / item[field]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.exists():
                errors.append(f"{identifier}: invalid {field}")
    for path in (root / "lessons").rglob("*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if any(cell.get("outputs") for cell in notebook.get("cells", [])):
            errors.append(f"{path.relative_to(root)}: notebook outputs must be cleared")
    return errors
