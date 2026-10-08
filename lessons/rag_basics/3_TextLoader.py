"""rag.03：加载 UTF-8 文本与查看元数据。无需 API 密钥。"""
from lessons.rag_basics.helpers import SAMPLE_DIR

def main():
    from langchain_community.document_loaders import TextLoader
    documents = TextLoader(str(SAMPLE_DIR / "beijing_guide.txt"), encoding="utf-8").load()
    for document in documents:
        print(document.metadata)
        print(document.page_content)

if __name__ == "__main__":
    main()
