from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage


class ChatHistoryManager:
    """负责单个会话的历史记录。"""

    def __init__(self, chat_session_id: str) -> None:
        self.chat_session_id = chat_session_id
        self._history = InMemoryChatMessageHistory()

    def get_history(self) -> BaseChatMessageHistory:
        return self._history

    def get_messages(self) -> list[BaseMessage]:
        return self._history.messages

    def add_user_message(self, content: str) -> None:
        self._history.add_user_message(content)

    def add_ai_message(self, content: str) -> None:
        self._history.add_ai_message(content)

    def get_recent_messages(self, count: int) -> list[BaseMessage]:
        return self._history.messages[-count:] if count > 0 else []

    def clear(self) -> None:
        self._history.clear()
