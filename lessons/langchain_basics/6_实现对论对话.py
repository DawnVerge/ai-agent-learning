"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.chat_models.tongyi import ChatTongyi


    class MultiTurnChat:
        def __init__(self, model: str, system_prompt: str = None):
            # 创建支持流式输出的模型客户端
            self.llm = ChatTongyi(
                model=model,
                streaming=True
            )
            # 使用二元组列表存储对话历史
            self.chat_history = []

            # 若提供了系统提示词，则将其添加至对话历史起始位置
            if system_prompt:
                self.chat_history.append(("system", system_prompt))

        def add_user_message(self, content: str) -> None:
            """添加用户消息（二元组形式）"""
            self.chat_history.append(("human", content))

        def add_ai_message(self, content: str) -> None:
            """添加助手消息（二元组形式）"""
            self.chat_history.append(("ai", content))

        def send(self, user_message: str):
            """发送消息并返回流式输出"""
            # 1. 添加用户消息到历史
            self.add_user_message(user_message)

            # 2. 直接使用二元组历史调用模型进行流式输出
            stream = self.llm.stream(input=self.chat_history)

            # 3. 收集完整回复并逐块返回
            full_reply = ""
            for chunk in stream:
                if chunk.content:
                    full_reply += chunk.content
                    yield chunk.content

            # 4. 添加模型的完整回复到历史
            self.add_ai_message(full_reply)

        def get_history(self):
            """获取当前对话历史（二元组形式）"""
            return self.chat_history.copy()


    if __name__ == '__main__':
        # 1. 配置参数
        MODEL = get_chat_model_name('qwen3-max')
        SYSTEM_MESSAGE = "背景设定：你现在是一个AI老师，负责上AI课程。"

        # 2. 创建多轮对话对象
        chat = MultiTurnChat(
            model=MODEL,
            system_prompt=SYSTEM_MESSAGE
        )

        print("多轮对话已启动，输入内容后按回车发送。输入 'exit' 或 'quit' 退出程序。")
        print(f"当前对话历史：{chat.get_history()}\n")

        # 3. 循环接受用户输入并且回答
        while True:
            # 获取用户输入
            user_input = input("用户: ")

            # 退出条件判断
            if user_input in ["exit", "quit"]:
                print("对话结束！拜拜~")
                print(f"最终对话历史：{chat.get_history()}")
                break

            # 跳过空的输入
            if not user_input.strip():
                print("请勿输入空白字符！")
                continue

            # 调用模型并且回复
            print("AI老师：", end="", flush=True)
            for chunk in chat.send(user_input):
                print(chunk, end='', flush=True)
            print()


if __name__ == "__main__":
    main()
