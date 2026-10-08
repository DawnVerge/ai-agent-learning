"""混合检索课程中的纯排序函数和自编样本。"""
import json
from lessons.rag_basics.helpers import SAMPLE_DIR, make_embeddings, cosine_similarity


def sample_documents():
    return json.loads((SAMPLE_DIR / "retrieval_documents.json").read_text(encoding="utf-8"))


def vector_search(query, docs, embeddings):
    query_embedding = embeddings.embed_query(query)
    document_embeddings = embeddings.embed_documents(docs)
    scores = [cosine_similarity(query_embedding, vector) for vector in document_embeddings]
    return sorted(enumerate(scores), key=lambda item: item[1], reverse=True)


def bm25_search(query, docs):
    import jieba
    from rank_bm25 import BM25Okapi
    tokenized = [list(jieba.cut(doc.strip())) for doc in docs]
    scores = BM25Okapi(tokenized).get_scores(list(jieba.cut(query.strip())))
    return sorted(enumerate(scores), key=lambda item: item[1], reverse=True)


def reciprocal_rank_fusion(rank_lists, k=60):
    """根据排名融合，避免直接相加量纲不同的向量与 BM25 分数。"""
    if k < 0:
        raise ValueError("k 不能小于零")
    fusion_scores = {}
    for rank_list in rank_lists:
        seen = set()
        for rank, (doc_id, _) in enumerate(rank_list, start=1):
            if doc_id in seen:
                continue
            seen.add(doc_id)
            fusion_scores[doc_id] = fusion_scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(fusion_scores.items(), key=lambda item: item[1], reverse=True)
