"""Command-line entry for the customer support learning project."""

import argparse


def main():
    parser = argparse.ArgumentParser(description="灵语客服：意图识别、历史摘要和关键事实记忆")
    parser.add_argument("--message", help="发送一条消息；不设置时进入多轮交互")
    parser.add_argument("--session", default="learning-session")
    args = parser.parse_args()
    from ai_learning.config import get_api_key, load_environment
    load_environment()
    get_api_key()
    from chat_service import ChatService
    from core.protocol import ChatRequest
    from uuid import uuid4

    service = ChatService()

    def ask(message):
        response = service.handle(ChatRequest(user_id="learner", chat_session_id=args.session,
                                             user_input=message, trace_id=str(uuid4())))
        print(response.response)

    if args.message:
        ask(args.message)
        return
    print("灵语客服学习示例，输入 exit 结束。业务操作为对话演示，不连接电商系统。")
    while True:
        try:
            message = input("你：").strip()
        except EOFError:
            break
        if message.lower() in {"exit", "quit"}:
            break
        if message:
            ask(message)


if __name__ == "__main__":
    main()
