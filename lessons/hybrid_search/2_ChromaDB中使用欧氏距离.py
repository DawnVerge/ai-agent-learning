"""hybrid.02：配置 Chroma 的 l2 距离。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_vectorstore
from lessons.hybrid_search.helpers import sample_documents

def main():
    db = make_vectorstore("hybrid_l2_demo", sample_documents(), space="l2")
    for document, distance in db.similarity_search_with_score("Aurora-4 的传感器数量", k=3):
        print(f"平方欧氏距离={distance:.4f}（越小越近） {document.page_content}")

if __name__ == "__main__":
    main()
