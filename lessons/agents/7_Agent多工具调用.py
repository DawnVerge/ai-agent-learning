"""演示有依赖关系的两次工具调用：商品名称 → ID → 价格。"""

import os

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

from ai_learning.config import get_api_key


PRODUCTS = {
    "示例手机": {"id": 101, "price": 3999},
    "示例电脑": {"id": 102, "price": 6999},
}


@tool
def get_product_id_by_name(name: str) -> int | None:
    """根据名称查询示例商品 ID。"""
    item = PRODUCTS.get(name)
    return item["id"] if item else None


@tool
def get_product_price_by_id(product_id: int) -> str:
    """根据 ID 查询示例商品价格。"""
    for name, item in PRODUCTS.items():
        if item["id"] == product_id:
            return f"{name}的示例价格为 {item['price']} 元。"
    return "未找到该商品。"


def main():
    get_api_key()
    agent = create_agent(
        model=ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")),
        tools=[get_product_id_by_name, get_product_price_by_id],
        system_prompt=(
            "先根据商品名称获取 ID，再用 ID 查询价格，最后告诉用户查询结果。"
            "如果商品不存在，明确说明，不要编造价格。"
        ),
    )
    result = agent.invoke({"messages": [("user", "示例手机的价格是多少？")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
