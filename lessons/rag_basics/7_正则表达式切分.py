"""rag.07：通过后向断言保留句末标点。无需 API 密钥。"""
def main():
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text = "社团项目持续六周。第一阶段学习模型调用！第二阶段实现文档检索？第三阶段增加离线测试；每组有三名成员。"
    splitter = RecursiveCharacterTextSplitter(chunk_size=35, chunk_overlap=0, is_separator_regex=True, separators=[r"(?<=。)", r"(?<=！)", r"(?<=？)", r"(?<=；)", ""])
    for chunk in splitter.split_text(text):
        print(chunk)

if __name__ == "__main__":
    main()
