"""PDF 问答的命令行入口。--help 不加载模型或建立索引。"""
import argparse
from pathlib import Path
from urllib.parse import urlparse
from ai_learning.config import PROJECT_ROOT, load_environment


def main(argv=None):
    parser = argparse.ArgumentParser(description="基于证据和页码的 PDF 问答；需要 DASHSCOPE_API_KEY。")
    parser.add_argument("--pdf", default=str(PROJECT_ROOT / "assets" / "learning_guide.pdf"), help="PDF 路径（相对仓库根目录）或 HTTP(S) URL")
    parser.add_argument("--question", default="社团项目周期是多久？", help="单轮问题；默认使用样本问题")
    parser.add_argument("--interactive", action="store_true", help="进入连续对话，输入 exit 或 quit 结束")
    args = parser.parse_args(argv)
    load_environment()
    from projects.smart_reading.run import PDFQA
    try:
        source = args.pdf
        if urlparse(source).scheme not in {"http", "https"}:
            path = Path(source).expanduser()
            source = str(path if path.is_absolute() else PROJECT_ROOT / path)
        qa = PDFQA(source)
        if not args.interactive:
            result = qa.ask(args.question)
            print(result["answer"])
            if result.get("error"):
                print(result["error"])
                return 1
            for index, evidence in enumerate(result["evidence"], 1):
                page = f"第 {evidence.page + 1} 页" if evidence.page is not None else "页码未知"
                print(f"[{index}] {evidence.source}，{page}")
            return 0
        print("输入问题开始连续对话；输入 exit 或 quit 结束。")
        while True:
            try:
                question = input("你：").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if question.lower() in {"exit", "quit"}:
                break
            if question:
                result = qa.ask(question)
                print("助手：" + result["answer"])
                if result.get("error"):
                    print(result["error"])
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"无法完成 PDF 问答：{exc}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
