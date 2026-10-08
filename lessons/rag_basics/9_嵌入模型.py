"""rag.09：生成一个查询向量。需要 DASHSCOPE_API_KEY。"""
from lessons.rag_basics.helpers import make_embeddings

def main():
    vector = make_embeddings().embed_query("社团项目持续多久？")
    print(f"向量维度：{len(vector)}")
    print(f"前 8 个元素：{vector[:8]}")

if __name__ == "__main__":
    main()
