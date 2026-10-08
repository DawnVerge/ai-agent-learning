"""hybrid.04：配置 Chroma 的余弦距离。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_vectorstore
from lessons.hybrid_search.helpers import sample_documents

def main():
    db = make_vectorstore("hybrid_cosine_demo", sample_documents(), space="cosine")
    for document, distance in db.similarity_search_with_score("Aurora-4 的传感器数量", k=3):
        print(f"余弦距离={distance:.4f}（越小越近） {document.page_content}")

if __name__ == "__main__":
    main()
