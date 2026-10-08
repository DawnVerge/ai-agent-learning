"""用工具调用中间件把异常转为模型可以理解的消息。"""

import os

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

from ai_learning.config import get_api_key


@tool
def get_weather(location: str) -> str:
    """演示天气工具；北京会触发一个预设错误。"""
    if location == "北京":
        raise ValueError("模拟服务暂时不可用")
    return f"{location}的模拟天气：晴，25°C。"


@wrap_tool_call
def handle_tool_errors(request, handler):
    """捕获工具异常并反馈给模型。"""
    try:
        return handler(request)
    except Exception as exc:
        return ToolMessage(
            content=f"工具执行失败：{exc}。请告诉用户当前无法获得天气。",
            tool_call_id=request.tool_call["id"],
        )


def main():
    get_api_key()
    agent = create_agent(
        model=ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")),
        tools=[get_weather],
        middleware=[handle_tool_errors],
    )
    result = agent.invoke({"messages": [("user", "北京的天气怎么样？")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
