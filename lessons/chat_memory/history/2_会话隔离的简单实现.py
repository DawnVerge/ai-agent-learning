"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from typing import Dict, List

    from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
    from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

    # 存储每个对话的历史消息：key是chat_session_id，value是会话历史记录
    _session_store: Dict[str, BaseChatMessageHistory] = {}


    class Memory:
        def get_session_history(self, chat_session_id: str) -> BaseChatMessageHistory:
            # 根据 chat_session_id 找到对应的会话历史记录
            if chat_session_id not in _session_store:
                _session_store[chat_session_id] = InMemoryChatMessageHistory()
            return _session_store[chat_session_id]

        def add_human_message(self, chat_session_id: str, message: str | HumanMessage) -> None:
            # 1.先获取对应的聊天历史对象
            chat_history = self.get_session_history(chat_session_id)
            # 2.添加人类消息
            if isinstance(message, str):
                chat_history.add_message(HumanMessage(message))
            else:
                chat_history.add_message(message)

        def add_ai_message(self, chat_session_id: str, message: str | AIMessage) -> None:
            # 1.先获取对应的聊天历史对象
            chat_history = self.get_session_history(chat_session_id)
            # 2.添加AI消息
            if isinstance(message, str):
                chat_history.add_message(AIMessage(message))
            else:
                chat_history.add_message(message)

        def messages(self, chat_session_id: str) -> List[BaseMessage]:
            return self.get_session_history(chat_session_id).messages


if __name__ == "__main__":
    main()
