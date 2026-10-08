"""手动完成模型请求工具、执行工具、反馈结果的单轮流程。"""

import os

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

from ai_learning.config import get_api_key


@tool
def get_weather(location: str) -> str:
    """返回某个城市的模拟天气，用来演示工具调用。"""
    return f"{location}的模拟天气：晴，25°C。此数据不是实时天气。"


def main():
    get_api_key()
    tools = [get_weather]
    model = ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")).bind_tools(tools)
    messages = [
        SystemMessage(content="你是天气助手。使用工具，并明确天气是模拟数据。"),
        HumanMessage(content="北京和上海的天气怎么样？"),
    ]
    response = model.invoke(messages)
    messages.append(response)
    tool_map = {item.name: item for item in tools}

    for call in response.tool_calls:
        try:
            result = tool_map[call["name"]].invoke(call["args"])
        except Exception as exc:
            result = f"工具调用失败：{exc}"
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    if response.tool_calls:
        response = model.invoke(messages)
    print(response.content)


if __name__ == "__main__":
    main()
