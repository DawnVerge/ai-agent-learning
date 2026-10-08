"""LangChain 从同目录 stdio MCP 服务发现并调用工具。"""

import asyncio
import os
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_mcp_adapters.client import MultiServerMCPClient

from ai_learning.config import get_api_key


async def main():
    get_api_key()
    server = Path(__file__).resolve().with_name("weather.py")
    client = MultiServerMCPClient({
        "weather": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(server)],
        }
    })
    tools = await client.get_tools()
    print("发现的工具：", ", ".join(item.name for item in tools))
    agent = create_agent(
        model=ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")),
        tools=tools,
        system_prompt="使用天气工具回答问题，并明确结果是模拟数据。",
    )
    result = await agent.ainvoke({"messages": [("user", "北京的天气怎么样？")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
