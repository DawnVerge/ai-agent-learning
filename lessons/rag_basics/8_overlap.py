"""rag.08：比较相邻块的重叠文本。无需 API 密钥。"""
def main():
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for overlap in [0, 3]:
        splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=overlap, separators=[""])
        print(f"overlap={overlap}: {splitter.split_text(text)}")

if __name__ == "__main__":
    main()
