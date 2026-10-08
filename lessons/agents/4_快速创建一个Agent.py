"""用 create_agent 自动完成工具执行与结果反馈。"""

import os

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

from ai_learning.config import get_api_key


@tool
def get_goods_info_by_id(goods_id: int) -> str:
    """根据商品 ID 返回内存中的示例商品。"""
    goods = {1: "示例手机", 2: "示例电脑"}
    return goods.get(goods_id, f"未找到 ID 为 {goods_id} 的商品。")


def main():
    get_api_key()
    agent = create_agent(
        model=ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")),
        tools=[get_goods_info_by_id],
        system_prompt="你是商品查询助手，请使用工具查询商品信息。",
    )
    result = agent.invoke({"messages": [("user", "商品 ID 为 1，这是什么商品？")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
