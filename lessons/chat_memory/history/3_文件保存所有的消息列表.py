"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    (PROJECT_ROOT / ".cache").mkdir(exist_ok=True)
    from langchain_community.chat_message_histories import FileChatMessageHistory

    session_id = "123"
    memory = FileChatMessageHistory(file_path=str(PROJECT_ROOT / ".cache" / f"{session_id}_session_store.json"), encoding="utf-8")

    memory.add_user_message("你是谁？")
    memory.add_ai_message("我是AI？")

    print(memory.messages)


if __name__ == "__main__":
    main()
