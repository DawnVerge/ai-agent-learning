"""Persist PDF indexes and reuse only completed builds."""

import hashlib
import json
from collections.abc import Callable

from filelock import FileLock
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document

from ..config.setting import QaConfig

INDEX_VERSION = 1


class VectorStoreManager:
    def __init__(self, config: QaConfig, embeddings: DashScopeEmbeddings):
        self._config = config
        self._embeddings = embeddings

    def _index_key(self, file_hash: str) -> str:
        settings = (
            INDEX_VERSION,
            file_hash,
            self._config.collection_prefix,
            self._config.embedding_model,
            self._config.chunk_size,
            self._config.chunk_overlap,
        )
        return hashlib.sha256(json.dumps(settings).encode("utf-8")).hexdigest()

    def load_or_build(
        self,
        file_hash: str,
        build_chunks: Callable[[], list[Document]] | None = None,
    ) -> Chroma:
        if not file_hash:
            raise ValueError("文件哈希不能为空")

        index_key = self._index_key(file_hash)
        persist_dir = self._config.chroma_root_dir / f"pdf_{index_key}"
        persist_dir.mkdir(parents=True, exist_ok=True)
        completed = persist_dir / ".complete"

        # Serialize builds for the same index, including retries after a partial write.
        with FileLock(str(persist_dir / ".build.lock")):
            vector_store = Chroma(
                collection_name=f"{self._config.collection_prefix}_{index_key}",
                embedding_function=self._embeddings,
                persist_directory=str(persist_dir),
                collection_metadata={"hnsw:space": "cosine"},
            )
            if completed.is_file() and vector_store.get(limit=1, include=[])["ids"]:
                return vector_store

            if build_chunks is None:
                raise ValueError("向量索引尚未构建完成")
            completed.unlink(missing_ok=True)
            chunks = build_chunks()
            if not chunks:
                raise ValueError("PDF切分后未生成任何文本块")
            vector_store.add_documents(
                documents=chunks,
                ids=[f"doc-{index}" for index in range(1, len(chunks) + 1)],
            )
            completed.touch()
            return vector_store
