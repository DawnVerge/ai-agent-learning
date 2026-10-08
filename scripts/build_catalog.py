"""Regenerate the example index after adding or renaming lessons."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_catalog():
    stages = [
        ("model-api", "lessons/model_api", set()),
        ("langchain", "lessons/langchain_basics", set()),
        ("prompts", "lessons/prompts", {5, 6, 7, 10}),
        ("history", "lessons/chat_memory/history", {1, 2, 3}),
        ("memory", "lessons/chat_memory/documents", {3, 4}),
        ("rag", "lessons/rag_basics", {1, 2, 3, 5, 6, 7, 8}),
        ("hybrid", "lessons/hybrid_search", {1, 3}),
        ("agents", "lessons/agents", set()),
    ]
    catalog = []
    for prefix, folder, offline in stages:
        numbered = []
        for path in (ROOT / folder).glob("*.py"):
            match = re.match(r"(\d+)_(.+)\.py$", path.name)
            if match:
                numbered.append((int(match.group(1)), match.group(2), path))
        for number, title, path in sorted(numbered):
            network = number not in offline
            catalog.append({"id": f"{prefix}.{number:02}", "title": title.replace("_", " "),
                            "path": path.relative_to(ROOT).as_posix(), "workdir": folder,
                            "api_key": network and not (prefix == "rag" and number == 4),
                            "network": network, "mysql": False,
                            "extra": "rag" if prefix in {"rag", "hybrid"} or (prefix == "memory" and number == 3) else "base"})
    special = [
        ("mcp.weather", "天气 MCP 服务（模拟数据，stdio）", "lessons/mcp/weather.py", "lessons/mcp", False, False, True, "mcp"),
        ("mcp.http", "Streamable HTTP MCP 服务", "lessons/mcp/Streamable_HTTP_01.py", "lessons/mcp", False, False, True, "mcp"),
        ("mcp.client", "LangChain 连接天气 MCP", "lessons/mcp/2_LangChain连接MCP_Server.py", "lessons/mcp", True, False, False, "mcp"),
        ("project.chat", "灵语客服：意图与记忆", "projects/lingyu_chat/cli.py", "projects/lingyu_chat", True, False, False, "base"),
        ("project.pdf-qa", "PDF 文档多轮问答", "projects/smart_reading/cli.py", "projects/smart_reading", True, False, False, "rag"),
        ("project.text-to-sql", "自然语言查询 MySQL", "projects/text_to_sql/db_tools.py", "projects/text_to_sql", True, True, False, "sql"),
        ("project.database-mcp", "数据库 MCP Agent", "projects/database_mcp/client.py", "projects/database_mcp", True, True, False, "mcp,sql"),
    ]
    for identifier, title, path, workdir, api, mysql, server, extra in special:
        catalog.append({"id": identifier, "title": title, "path": path, "workdir": workdir,
                        "api_key": api, "network": api, "mysql": mysql, "server": server, "extra": extra,
                        "accepts_arguments": path.endswith("/cli.py")})
    (ROOT / "ai_learning/catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(catalog)} examples.")


if __name__ == "__main__":
    build_catalog()
