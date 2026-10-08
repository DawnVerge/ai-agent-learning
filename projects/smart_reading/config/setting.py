"""PDF 问答配置。路径基于仓库根目录，不依赖启动位置。"""
from dataclasses import dataclass, field
from pathlib import Path
import os
from ai_learning.config import PROJECT_ROOT, get_chat_model_name

@dataclass
class QaConfig:
    chunk_size: int = 200
    chunk_overlap: int = 20
    chroma_root_dir: Path = field(default_factory=lambda: PROJECT_ROOT / ".cache" / "smart_reading" / "chroma")
    collection_prefix: str = "pdf_qa"
    embedding_model: str = field(default_factory=lambda: os.getenv("DASHSCOPE_EMBEDDING_MODEL", "text-embedding-v1"))
    chat_model: str = field(default_factory=get_chat_model_name)

    def __post_init__(self):
        if self.chunk_size <= 0 or not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("chunk_size 必须为正数，且 chunk_overlap 必须小于 chunk_size")
        self.chroma_root_dir = Path(self.chroma_root_dir).expanduser().resolve()
