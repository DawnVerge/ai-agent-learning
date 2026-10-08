"""rag.05：按段落分隔符切分，与下一课的递归切分比较。无需 API 密钥。"""
from lessons.rag_basics.helpers import SAMPLE_DIR

def main():
    from langchain_text_splitters import CharacterTextSplitter
    text = (SAMPLE_DIR / "history_note.txt").read_text(encoding="utf-8")
    splitter = CharacterTextSplitter(separator="\n\n", chunk_size=80, chunk_overlap=0)
    for index, chunk in enumerate(splitter.split_text(text), 1):
        print(f"块 {index}，长度 {len(chunk)}：{chunk}")
    print("单段过长时 CharacterTextSplitter 可能超过目标长度；下一课递归使用更多分隔符。")

if __name__ == "__main__":
    main()
