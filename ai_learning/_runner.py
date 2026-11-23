"""Execute one example in an isolated process with predictable imports and cwd."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

from .config import PROJECT_ROOT, load_environment


def main() -> None:
    script = (PROJECT_ROOT / sys.argv[1]).resolve()
    workdir = (PROJECT_ROOT / sys.argv[2]).resolve()
    extra = sys.argv[3]
    if not script.is_relative_to(PROJECT_ROOT) or not workdir.is_relative_to(PROJECT_ROOT):
        raise ValueError("Example paths must stay inside this repository.")
    if not script.is_file() or not workdir.is_dir():
        raise ValueError("Example file or working directory does not exist.")
    load_environment()
    sys.path[:0] = [str(script.parent), str(workdir), str(PROJECT_ROOT)]
    sys.argv = [str(script), *sys.argv[4:]]
    os.chdir(workdir)
    try:
        runpy.run_path(str(script), run_name="__main__")
    except ImportError as error:
        missing = error if isinstance(error, ModuleNotFoundError) else error.__cause__ or error.__context__
        if not isinstance(missing, ModuleNotFoundError) or not missing.name:
            raise
        if missing.name.split(".", 1)[0] in {"ai_learning", "lessons", "projects"}:
            raise
        install = "." if extra == "base" else f".[{extra}]"
        raise SystemExit(f'缺少 Python 模块 {missing.name}，请在仓库根目录运行 python -m pip install -e "{install}"') from None


if __name__ == "__main__":
    main()
