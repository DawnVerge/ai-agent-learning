"""Browse and run lessons without importing paid or optional integrations."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path

from .config import PROJECT_ROOT, get_api_key, load_environment, mysql_settings


def get_catalog() -> list[dict]:
    return json.loads(Path(__file__).with_name("catalog.json").read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AI Agent Learning: lessons and practical projects")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="List available examples")
    listing.add_argument("--offline", action="store_true", help="Only examples without API or internet requirements")
    running = commands.add_parser("run", help="Run an example in a separate process")
    running.add_argument("id", help="Example id from the list command")
    running.add_argument("arguments", nargs=argparse.REMAINDER, help="Arguments passed to the example")
    commands.add_parser("doctor", help="Show environment and optional dependency status (no secrets)")
    commands.add_parser("check", help="Validate repository syntax, configuration and catalog offline")
    args = parser.parse_args(argv)
    if args.command == "check":
        from .validation import check_repository
        errors = check_repository()
        for error in errors:
            print(error, file=sys.stderr)
        print(f"Repository checks: {'FAILED' if errors else 'OK'}")
        return int(bool(errors))
    if args.command == "list":
        for item in get_catalog():
            if args.offline and (item["network"] or item["mysql"] or item.get("server")):
                continue
            flags = [name for name, enabled in (("API", item["api_key"]), ("MySQL", item["mysql"]),
                                                 ("server", item.get("server"))) if enabled]
            print(f"{item['id']:<25} {item['title']}" + (f"  [{', '.join(flags)}]" if flags else ""))
        return 0
    try:
        load_environment()
        if args.command == "doctor":
            print(f"Python: {sys.version.split()[0]} | supported: 3.11-3.13")
            print(f"Repository: {PROJECT_ROOT}")
            try:
                get_api_key()
                configured = True
            except ValueError:
                configured = False
            print(f"API key: {'configured' if configured else 'not configured (offline lessons still work)'}")
            for package in ("openai", "langchain", "langchain-community", "dashscope", "langchain-chroma", "mcp", "sqlalchemy"):
                try:
                    status = importlib.metadata.version(package)
                except importlib.metadata.PackageNotFoundError:
                    status = "not installed"
                print(f"{package}: {status}")
            return 0
        item = next((item for item in get_catalog() if item["id"] == args.id), None)
        if item is None:
            parser.error(f"Unknown example: {args.id}. Use 'python -m ai_learning list'.")
        arguments = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
        help_only = "--help" in arguments or "-h" in arguments
        if not item.get("accepts_arguments"):
            if help_only:
                print(f"{item['id']}: {item['title']}\nFile: {item['path']}\nDependencies: {item['extra']}")
                print("This lesson takes no command-line arguments. Run it without --help to execute it.")
                return 0
            if arguments:
                parser.error(f"{item['id']} does not accept arguments.")
        if not help_only:
            if item["api_key"]:
                get_api_key()
            if item["mysql"]:
                mysql_settings()
        result = subprocess.run([sys.executable, "-m", "ai_learning._runner", item["path"], item["workdir"], *arguments],
                                cwd=PROJECT_ROOT, check=False)
        return result.returncode
    except (ValueError, OSError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130
