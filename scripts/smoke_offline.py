"""Run catalogued offline lessons without model credentials or API calls."""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    environment = {key: value for key, value in os.environ.items() if not key.endswith("API_KEY")}
    environment["LANGSMITH_TRACING"] = "false"
    catalog = json.loads((ROOT / "ai_learning/catalog.json").read_text(encoding="utf-8"))
    examples = [item for item in catalog if not item["network"] and not item["mysql"] and not item.get("server")]
    failed = []
    for item in examples:
        result = subprocess.run([sys.executable, "-m", "ai_learning", "run", item["id"]],
                                cwd=ROOT, env=environment, text=True, encoding="utf-8", errors="replace",
                                capture_output=True, timeout=45)
        print(f"{'OK' if result.returncode == 0 else 'FAIL'} {item['id']}")
        if result.returncode:
            failed.append(item["id"])
            print(result.stderr[-1500:])
    print(f"Offline examples: {len(examples) - len(failed)}/{len(examples)} passed")
    return int(bool(failed))


if __name__ == "__main__":
    raise SystemExit(main())
