"""rag.06：按中文段落和标点递归切分。无需 API 密钥。"""
from lessons.rag_basics.helpers import SAMPLE_DIR

def main():
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text = (SAMPLE_DIR / "history_note.txt").read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=80, chunk_overlap=10, separators=["\n\n", "\n", "。", "，", " ", ""])
    for i, chunk in enumerate(splitter.split_text(text), 1):
        print(f"块 {i}，长度 {len(chunk)}：{chunk}")

if __name__ == "__main__":
    main()
