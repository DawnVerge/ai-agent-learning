"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.chat_models.tongyi import ChatTongyi
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from typing import Dict
    from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory

    # ========== 会话存储 ==========
    _session_store: Dict[str, BaseChatMessageHistory] = {}


    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in _session_store:
            _session_store[session_id] = InMemoryChatMessageHistory()
        return _session_store[session_id]


    # ========== 构建链 ==========
    model = ChatTongyi(model=get_chat_model_name('qwen3-max'), streaming=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个友好的AI助手。"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    parser = StrOutputParser()

    chain = prompt | model | parser

    # ========== 包装为带历史的链 ==========
    wrapped_chain = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    # ========== 测试代码 ==========
    if __name__ == "__main__":
        session_id = "user_001"

        print("用户: 你好，我叫阿苑")
        print("AI: ", end='', flush=True)
        for chunk in wrapped_chain.stream(
                {"input": "你好，我叫阿苑"},
                config={"configurable": {"session_id": session_id}}
        ):
            print(chunk, end='', flush=True)
        print()

        print("用户: 我叫什么名字？")
        print("AI: ", end='', flush=True)
        for chunk in wrapped_chain.stream(
                {"input": "我叫什么名字？"},
                config={"configurable": {"session_id": session_id}}
        ):
            print(chunk, end='', flush=True)
        print()


if __name__ == "__main__":
    main()
