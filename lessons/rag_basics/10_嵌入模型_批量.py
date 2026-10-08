"""rag.10：批量生成文档向量。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_embeddings

def main():
    texts = ["社团项目持续六周。", "每组有三名成员。", "评审员检查引用页码。"]
    vectors = make_embeddings().embed_documents(texts)
    for text, vector in zip(texts, vectors):
        print(text, "维度：", len(vector), "前 3 项：", vector[:3])

if __name__ == "__main__":
    main()
