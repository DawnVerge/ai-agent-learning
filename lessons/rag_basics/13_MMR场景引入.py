"""rag.13：观察相似度检索中相近内容重复出现。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_vectorstore, learning_documents

def main():
    db = make_vectorstore("rag_mmr_demo", learning_documents())
    for document, score in db.similarity_search_with_relevance_scores("如何学习人工智能？", k=3):
        print(f"{score:.4f} {document.page_content}")

if __name__ == "__main__":
    main()
