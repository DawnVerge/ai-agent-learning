"""数据库 MCP stdio 服务入口。"""

import sys
from pathlib import Path

# MCP 子进程按绝对脚本路径启动，也能找到根目录的配置模块。
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_learning.config import load_environment
from mcp_tools import mcp


def main():
    load_environment()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
