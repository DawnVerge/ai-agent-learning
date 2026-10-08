"""rag.02：逐页加载项目自编 PDF。无需 API 密钥。"""
from lessons.rag_basics.helpers import SAMPLE_DIR

def main():
    from langchain_community.document_loaders import PyMuPDFLoader
    loader = PyMuPDFLoader(str(SAMPLE_DIR / "learning_guide.pdf"))
    documents = loader.load()
    print(f"共 {len(documents)} 页")
    for document in loader.lazy_load():
        print(document.metadata)
        print(document.page_content[:120])

if __name__ == "__main__":
    main()
