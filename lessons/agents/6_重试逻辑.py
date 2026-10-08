"""对工具的临时错误最多尝试三次，失败后返回错误消息。"""

import os
import time

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

from ai_learning.config import get_api_key


@tool
def get_weather(location: str) -> str:
    """演示天气工具；北京会持续触发预设错误以展示重试。"""
    if location == "北京":
        raise ValueError("模拟服务暂时不可用")
    return f"{location}的模拟天气：晴，25°C。"


@wrap_tool_call
def retry_tool_call(request, handler):
    """只重试工具执行；总共三次尝试，间隔一秒。"""
    for attempt in range(1, 4):
        try:
            return handler(request)
        except Exception as exc:
            print(f"第 {attempt}/3 次尝试失败：{exc}")
            if attempt < 3:
                time.sleep(1)
            else:
                return ToolMessage(
                    content="工具多次尝试后仍失败，请告知用户稍后重试。",
                    tool_call_id=request.tool_call["id"],
                )


def main():
    get_api_key()
    agent = create_agent(
        model=ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")),
        tools=[get_weather],
        middleware=[retry_tool_call],
    )
    result = agent.invoke({"messages": [("user", "北京的天气怎么样？")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
