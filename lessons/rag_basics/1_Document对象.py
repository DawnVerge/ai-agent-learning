"""rag.01：用 Document 保存正文与来源元数据。无需 API 密钥。"""
def main():
    from langchain_core.documents import Document
    document = Document(page_content="星河社团每个项目持续六周。", metadata={"source": "自编教学样本", "page": 0})
    print(document.page_content)
    print(document.metadata)

if __name__ == "__main__":
    main()
