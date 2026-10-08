"""RAG 课程共享的样本与模型创建函数。导入本模块不会联网。"""
from pathlib import Path
from ai_learning.config import PROJECT_ROOT, get_api_key, load_environment

SAMPLE_DIR = PROJECT_ROOT / "assets"


def make_embeddings():
    from langchain_community.embeddings import DashScopeEmbeddings
    import os
    load_environment()
    return DashScopeEmbeddings(
        model=os.getenv("DASHSCOPE_EMBEDDING_MODEL", "text-embedding-v1"),
        dashscope_api_key=get_api_key(),
    )


def make_vectorstore(name, texts, space="cosine"):
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    db = Chroma(
        collection_name=name,
        persist_directory=str(PROJECT_ROOT / ".cache" / "rag_basics" / name),
        embedding_function=make_embeddings(),
        collection_metadata={"hnsw:space": space},
    )
    db.add_documents(
        [Document(page_content=text) for text in texts],
        ids=[f"sample-{i}" for i in range(len(texts))],
    )
    return db


def learning_documents():
    return [
        "学习人工智能需要先练习矩阵运算、概率统计和 Python 编程。",
        "AI 学习的基础包括线性代数、概率论以及程序设计。",
        "Python 开发者可以通过小项目练习文档检索与模型调用。",
        "组建读书小组，讨论材料来源和实验记录，有助于保持学习节奏。",
        "完成一个命令行问答程序，然后给它增加检索功能和离线测试。",
        "周末做饭前先准备食材，检查厨房里的调味料。",
    ]


def cosine_similarity(a, b):
    from math import sqrt
    if len(a) != len(b) or not a:
        raise ValueError("向量长度必须相同且不能为空")
    denominator = sqrt(sum(x*x for x in a) * sum(y*y for y in b))
    if denominator == 0:
        raise ValueError("零向量没有定义余弦相似度")
    return sum(x*y for x, y in zip(a, b)) / denominator
