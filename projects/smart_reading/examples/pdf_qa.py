"""手动联网演示：两轮问题与对话指代。"""
from ai_learning.config import PROJECT_ROOT, load_environment

def main():
    from projects.smart_reading.run import PDFQA
    load_environment()
    qa = PDFQA(str(PROJECT_ROOT / "assets" / "learning_guide.pdf"))
    for question in ["社团项目周期是多久？", "它的第二阶段要完成什么？"]:
        result = qa.ask(question)
        print("问题：", question)
        print("回答：", result["answer"])
        if result.get("error"):
            print(result["error"])
            break

if __name__ == "__main__":
    main()
