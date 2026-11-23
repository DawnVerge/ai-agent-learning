class FactManager:
    """负责单个会话的关键事实（Slots）。"""

    def __init__(self, chat_session_id: str) -> None:
        self.chat_session_id = chat_session_id
        self._facts: dict[str, str] = {}

    def get_all_facts(self) -> dict[str, str]:
        return self._facts.copy()

    def get_fact(self, key: str) -> str:
        return self._facts.get(key, "")

    def update_facts(self, facts: dict[str, str]) -> None:
        self._facts.update({key: value for key, value in facts.items() if value})

    def set_fact(self, key: str, value: str) -> None:
        if value:
            self._facts[key] = value

    def clear_facts(self) -> None:
        self._facts.clear()

    def delete_session(self) -> None:
        self.clear_facts()
