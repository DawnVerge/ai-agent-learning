"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.embeddings import DashScopeEmbeddings
    import numpy as np

    def euclidean_distance(a, b):
        """计算欧氏距离"""
        return np.linalg.norm(np.array(a) - np.array(b))

    if __name__ == '__main__':
        # 准备三个测试文本：前两个语义相近，第三个语义无关
        texts = ["猫坐在垫子上", "一只猫在垫子上休息", "今天天气很好"]
        vectors = DashScopeEmbeddings().embed_documents(texts)

        # 计算欧氏距离并观察结果
        print(f"'{texts[0]}' 与 '{texts[1]}' 的欧氏距离: {euclidean_distance(vectors[0], vectors[1])}")
        print(f"'{texts[0]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(vectors[0], vectors[2])}")
        print(f"'{texts[1]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(vectors[1], vectors[2])}")

    """
    '猫坐在垫子上' 与 '一只猫在垫子上休息' 的欧氏距离: 53.30557172891227
    '猫坐在垫子上' 与 '今天天气很好' 的欧氏距离: 115.3968429781511
    '一只猫在垫子上休息' 与 '今天天气很好' 的欧氏距离: 113.25200288012354
    """


if __name__ == "__main__":
    main()
