"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.document_loaders import PyMuPDFLoader

    file_path = str(PROJECT_ROOT / "assets/learning_guide.pdf")
    # 1.获取PDF文档内容
    docs = PyMuPDFLoader(file_path).load()
    # 2. 打印PDF文档内容
    for doc in docs:
        print(doc.page_content)


if __name__ == "__main__":
    main()
