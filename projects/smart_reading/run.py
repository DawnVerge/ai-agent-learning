"""逐条消息调用的 PDF 问答接口。首次 ask 时构建索引。"""
from typing import Any, Dict, Optional
from langchain_core.chat_history import InMemoryChatMessageHistory
from ai_learning.config import get_api_key
from .config.setting import QaConfig
from .indexing.indexing_pipeline import IndexingPipeline
from .querying.query_pipeline import RagPipeline

class PDFQA:
    def __init__(self, pdf_source: str, api_key: Optional[str] = None, config: Optional[QaConfig] = None):
        self.pdf_source = str(pdf_source)
        self.api_key = api_key or get_api_key()
        self.cfg = config or QaConfig()
        self.file_hash: Optional[str] = None
        self.chat_history = InMemoryChatMessageHistory()
        self.rag: Optional[RagPipeline] = None

    def _build_index(self) -> None:
        if self.file_hash is not None:
            return
        indexer = IndexingPipeline(self.cfg)
        self.file_hash = indexer.build_from_source(self.pdf_source, self.api_key)
        self.rag = RagPipeline(self.cfg)

    def ask(self, question: str) -> Dict[str, Any]:
        question = question.strip()
        if not question:
            raise ValueError("问题不能为空")
        if self.file_hash is None:
            self._build_index()
        result = self.rag.query(
            dashscope_api_key=self.api_key,
            file_hash=self.file_hash,
            question=question,
            chat_history=self.chat_history.messages,
            top_k=4,
            recall_k=10,
        )
        # 失败的服务响应不应污染下一轮对话。
        if not result.get("error"):
            self.chat_history.add_user_message(question)
            self.chat_history.add_ai_message(result["answer"])
        return result
