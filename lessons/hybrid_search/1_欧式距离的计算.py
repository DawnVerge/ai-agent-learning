"""hybrid.01：用小向量计算欧氏距离。无需 API 密钥。"""
from math import dist

def main():
    query = [1.0, 0.0, 0.0]
    documents = [[0.9, 0.1, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 0.0]]
    print("欧氏距离越小越接近；向量的长度也会影响结果。")
    for index, vector in enumerate(documents, 1):
        print(f"向量 {index}: {vector}，距离={dist(query, vector):.4f}")

if __name__ == "__main__":
    main()
