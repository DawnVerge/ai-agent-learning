"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.embeddings import DashScopeEmbeddings

    # 1.创建嵌入模型对象
    embedding = DashScopeEmbeddings()

    # 2.向量化
    vector = embedding.embed_query("需要被向量化的文本")

    # 3.处理输出
    print(vector)
    print(len(vector))


if __name__ == "__main__":
    main()
