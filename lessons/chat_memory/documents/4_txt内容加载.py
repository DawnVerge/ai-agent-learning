"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.document_loaders import TextLoader

    file_path = str(PROJECT_ROOT / "assets/beijing_guide.txt")
    # 1.获取TXT文档内容
    docs = TextLoader(file_path, encoding="utf-8").load()
    # 2. 打印TXT文档内容
    for doc in docs:
        print(doc.page_content)


if __name__ == "__main__":
    main()
