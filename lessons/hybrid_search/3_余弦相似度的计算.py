"""hybrid.03：用小向量计算余弦相似度。无需 API 密钥。"""
from lessons.rag_basics.helpers import cosine_similarity

def main():
    query = [1.0, 0.0, 0.0]
    documents = [[0.9, 0.1, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 0.0]]
    print("余弦相似度越大越相似；同方向的不同长度向量相似度相同。")
    for index, vector in enumerate(documents, 1):
        print(f"向量 {index}: {vector}，相似度={cosine_similarity(query, vector):.4f}")

if __name__ == "__main__":
    main()
