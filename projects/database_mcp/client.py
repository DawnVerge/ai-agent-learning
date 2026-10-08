"""通过当前 Python 解释器启动同目录数据库 MCP 服务。"""

import asyncio
import os
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_mcp_adapters.client import MultiServerMCPClient

from ai_learning.config import get_api_key, mysql_settings


async def main():
    get_api_key()
    mysql_settings()
    server = Path(__file__).resolve().with_name("mcp_db_server.py")
    client = MultiServerMCPClient({
        "database": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(server)],
        }
    })
    tools = await client.get_tools()
    agent = create_agent(
        model=ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")),
        tools=tools,
        system_prompt=(
            "你是只读数据库查询助手。先查看表名和表结构，再生成一条 SELECT 查询。"
            "不能修改数据库；默认限制结果数量。根据实际结果用中文回答，失败时不要编造。"
        ),
    )
    question = "销量排名前 5 的商品是哪些？"
    print(f"用户：{question}")
    result = await agent.ainvoke({"messages": [("user", question)]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
