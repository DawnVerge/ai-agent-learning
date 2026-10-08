"""观察模型在没有实时工具时如何回答天气问题。"""

import os

from langchain_community.chat_models import ChatTongyi

from ai_learning.config import get_api_key


def main():
    get_api_key()
    llm = ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max"))
    response = llm.invoke("明天北京的天气怎么样？请说明信息来源和时效性。")
    print(response.content)


if __name__ == "__main__":
    main()
