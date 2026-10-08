"""rag.14：比较相似度检索与 MMR 的结果多样性。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_vectorstore, learning_documents

def main():
    db = make_vectorstore("rag_mmr_demo", learning_documents())
    query = "如何学习人工智能？"
    print("普通相似度检索：")
    for document in db.similarity_search(query, k=3):
        print(document.page_content)
    print("MMR，lambda_mult=0.6：")
    for document in db.max_marginal_relevance_search(query, k=3, fetch_k=5, lambda_mult=0.6):
        print(document.page_content)

if __name__ == "__main__":
    main()
