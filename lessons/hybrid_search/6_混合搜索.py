"""hybrid.06：向量检索 + BM25 + RRF。需要 DASHSCOPE_API_KEY。"""
from lessons.hybrid_search.helpers import (
    sample_documents, make_embeddings, vector_search, bm25_search, reciprocal_rank_fusion,
)

def main():
    documents = sample_documents()
    query = "Aurora-4 的传感器数量"
    vector_results = vector_search(query, documents, make_embeddings())
    keyword_results = bm25_search(query, documents)
    fused_results = reciprocal_rank_fusion([vector_results, keyword_results])
    print("查询：", query, "；设备与数据均为虚构教学样本。")
    for title, results in [("向量相似度", vector_results), ("BM25 分数", keyword_results), ("RRF 融合分数", fused_results)]:
        print("\n" + title)
        for index, score in results:
            print(f"文档 {index}，{score:.4f}：{documents[index]}")

if __name__ == "__main__":
    main()
