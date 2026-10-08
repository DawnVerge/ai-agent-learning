"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.messages import HumanMessage, AIMessage

    # 1.创建 InMemoryChatMessageHistory 对象
    memory = InMemoryChatMessageHistory()

    # 2.添加消息
    memory.add_message(HumanMessage("你是谁？"))
    memory.add_message(AIMessage("我是AI。"))

    # 3.获取消息列表
    print(memory.messages)

    # 4.清空记忆
    memory.clear()


if __name__ == "__main__":
    main()
