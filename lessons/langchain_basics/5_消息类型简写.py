"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.chat_models.tongyi import ChatTongyi
    from langchain_core.messages import SystemMessage, HumanMessage

    # 1. 创建模型的客户端 —— 在这里加上 streaming=True
    llm = ChatTongyi(
        model=get_chat_model_name('qwen3-max'),
        streaming=True
    )

    # 2. 准备上下文 + 当前用户消息
    chat_history = [
        ("system", "背景设定：你现在是一个AI老师，负责上AI课程。"),
        ("human", "你是谁？")
    ]

    # 3. 携带上下文去调用模型
    result = llm.stream(input=chat_history)

    # 4. 处理输出
    for chunk in result:
        print(chunk.content, end='', flush=True)


if __name__ == "__main__":
    main()
