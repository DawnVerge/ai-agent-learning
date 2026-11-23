"""Load PDF pages and split them into chunks for retrieval."""

from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.parsers.pdf import PyMuPDFParser
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..config.setting import QaConfig


class PdfIngestor:
    # Bump the index version in vectorstorage.py when these parsing rules change.
    SEPARATORS = ["\n", "(?<=。)", "(?<=！)", "(?<=？)", "(?<=；)", "(?<=，)", " ", ""]

    def __init__(self, config: QaConfig) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            is_separator_regex=True,
            separators=self.SEPARATORS,
        )

    def ingest(self, pdf_source: str, pdf_bytes: bytes) -> list[Document]:
        blob = Blob.from_data(pdf_bytes, path=pdf_source, mime_type="application/pdf")
        documents = PyMuPDFParser().parse(blob)
        return self._splitter.split_documents(documents)
