"""hybrid.05：观察精确型号查询中的语义检索结果。需要 DASHSCOPE_API_KEY。"""
from lessons.hybrid_search.helpers import sample_documents, vector_search, make_embeddings

def main():
    documents = sample_documents()
    query = "Aurora-4 的传感器数量"
    print("查询：", query, "；以下设备与数据均为虚构教学样本。")
    for index, score in vector_search(query, documents, make_embeddings()):
        print(f"{score:.4f} {documents[index]}")
    print("观察相近型号是否混淆；下一课加入关键词检索与排名融合。")

if __name__ == "__main__":
    main()
