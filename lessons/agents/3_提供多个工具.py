"""观察同一次模型响应中出现的多个工具请求。"""

import os

from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

from ai_learning.config import get_api_key


@tool
def get_weather(location: str) -> str:
    """返回城市的模拟天气。"""
    return f"{location}的模拟天气：晴，25°C。"


@tool
def get_recommendations(city: str) -> str:
    """返回城市景点的静态示例数据。"""
    places = {"北京": "故宫、长城、颐和园", "上海": "外滩、豫园", "杭州": "西湖、灵隐寺"}
    return places.get(city, f"示例中没有{city}的景点。")


def main():
    get_api_key()
    model = ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")).bind_tools(
        [get_weather, get_recommendations]
    )
    response = model.invoke("北京的天气怎么样？有什么景点？")
    print("本课观察工具请求；下一课由 Agent 自动执行工具。")
    for call in response.tool_calls:
        print(f"{call['name']}: {call['args']}")
    if response.content:
        print(response.content)


if __name__ == "__main__":
    main()
