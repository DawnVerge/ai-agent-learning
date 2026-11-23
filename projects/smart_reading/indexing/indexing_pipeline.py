"""Build or reuse the Chroma index for a PDF."""

from langchain_community.embeddings import DashScopeEmbeddings

from ..config.setting import QaConfig
from .ingest import PdfIngestor
from .storage import PdfBytesStore
from .vectorstorage import VectorStoreManager


class IndexingPipeline:
    def __init__(self, config: QaConfig):
        self._config = config
        self._store = PdfBytesStore()

    def build_from_source(self, pdf_source: str, dashscope_api_key: str) -> str:
        """Return the content hash after ensuring the configured index exists."""
        if not pdf_source:
            raise ValueError("PDF源不能为空")
        if not dashscope_api_key:
            raise ValueError("DashScope API Key不能为空")

        pdf_bytes = self._store.read(pdf_source)
        file_hash = self._store.compute_hash(pdf_bytes)
        embeddings = DashScopeEmbeddings(
            model=self._config.embedding_model,
            dashscope_api_key=dashscope_api_key,
        )
        manager = VectorStoreManager(self._config, embeddings)
        manager.load_or_build(
            file_hash,
            build_chunks=lambda: PdfIngestor(self._config).ingest(pdf_source, pdf_bytes),
        )
        return file_hash
