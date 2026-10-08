"""rag.11：用余弦相似度对文档排序。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_embeddings, cosine_similarity

def main():
    query = "项目需要多长时间？"
    texts = ["社团项目持续六周。", "每组安排三名成员。", "完成全部阶段需要一个半月左右。"]
    model = make_embeddings()
    query_vector = model.embed_query(query)
    results = [(cosine_similarity(query_vector, vector), text) for text, vector in zip(texts, model.embed_documents(texts))]
    for score, text in sorted(results, reverse=True):
        print(f"{score:.4f} {text}")

if __name__ == "__main__":
    main()
