"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from openai import OpenAI

    class MultiTurnChat:
        """
        多轮对话管理类
        用于封装大模型对话历史维护与调用逻辑
        """

        def __init__(self, base_url: str, model: str, system_prompt: str = None):
            """
            初始化客户端与对话历史
            参数说明：
                base_url: API 服务地址
                model: 模型名称
                system_prompt: 系统提示词（可选），用于设定模型角色与行为规范
            """
            self.client = OpenAI(api_key=get_api_key(), base_url=base_url)
            self.model = model
            self.chat_history = []

            # 若提供了系统提示词，则将其添加至对话历史起始位置
            if system_prompt:
                self.chat_history.append({"role": "system", "content": system_prompt})

        def add_user_message(self, content: str) -> None:
            """添加用户消息至对话历史"""
            self.chat_history.append({"role": "user", "content": content})

        def add_assistant_message(self, content: str) -> None:
            """添加助手（模型）消息至对话历史"""
            self.chat_history.append({"role": "assistant", "content": content})

        def send(self, user_message: str) -> str:
            """
            发送用户消息，调用模型，返回回复内容，并自动更新对话历史
            参数说明：
                user_message: 用户输入的消息内容
            返回值：
                model_reply: 模型返回的回复文本
            """
            # 将用户消息加入历史
            self.add_user_message(user_message)
            # 调用模型
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_history
            )
            # 提取模型回复内容
            model_reply = completion.choices[0].message.content
            # 将模型回复加入历史
            self.add_assistant_message(model_reply)
            return model_reply

        def get_history(self) -> list:
            """获取完整的对话历史"""
            return self.chat_history


    # ========== 使用示例（支持用户动态输入） ==========
    if __name__ == "__main__":
        # 1. 配置参数
        BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        MODEL = get_chat_model_name('qwen3-max')
        SYSTEM_PROMPT = "背景设定：你现在是一个AI老师，负责上AI课程。"

        # 2. 创建多轮对话实例
        chat = MultiTurnChat(
            base_url=BASE_URL,
            model=MODEL,
            system_prompt=SYSTEM_PROMPT
        )

        print("多轮对话已启动，输入内容后按回车发送。输入 'exit' 或 'quit' 退出程序。\n")
        # 3. 循环接收用户输入
        while True:
            # 获取用户输入
            user_input = input("用户：")
            # 退出条件判断
            if user_input.lower() in ["exit", "quit"]:
                print("对话结束。")
                break
            # 跳过空输入
            if not user_input.strip():
                print("请勿输入空白内容。\n")
                continue
            # 调用模型并获取回复
            reply = chat.send(user_input)
            # 输出模型回复
            print(f"AI老师：{reply}\n")


if __name__ == "__main__":
    main()
