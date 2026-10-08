"""rag.12：演示 Chroma 新增、查询与删除。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_vectorstore

def main():
    db = make_vectorstore("rag_chroma_demo", ["社团项目持续六周。", "每组有三名成员。", "评估题共有十二道。"])
    print(db.similarity_search("一组有多少人？", k=1))
    db.delete(ids=["sample-1"])
    print("已删除 sample-1；再次运行会重新加入演示数据。")

if __name__ == "__main__":
    main()
