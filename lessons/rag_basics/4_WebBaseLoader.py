"""rag.04：加载官方文档网页。需要网络，无需模型 API 密钥。"""
def main():
    from langchain_community.document_loaders import WebBaseLoader
    documents = WebBaseLoader("https://docs.langchain.com/oss/python/langchain/overview").load()
    for document in documents:
        print(document.metadata)
        print(f"正文长度：{len(document.page_content)}")
        print(document.page_content[:300])

if __name__ == "__main__":
    main()
