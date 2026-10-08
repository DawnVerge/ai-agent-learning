"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.chat_models import ChatTongyi

    # =========================
    # 演示：通过注入对话历史，让大模型“有记忆”
    # =========================

    # 1. 创建通义千问客户端
    llm = ChatTongyi(model=get_chat_model_name('qwen3-max'))

    # 2. 定义对话历史
    chat_history = []

    # 3. 第一次调用：用户自我介绍
    user_message_1 = "你好，我是阿苑，是一个AI老师"
    chat_history.append(("user", user_message_1))      # 记录用户消息

    ai_reply_1 = llm.invoke(chat_history[-1][1])       # 调用模型
    chat_history.append(("ai", ai_reply_1))     # 记录AI回复
    print("第一次AI回复：", ai_reply_1)

    # 4. 第二次调用：询问“我是谁？”—— 携带完整历史
    user_message_2 = "我是谁？"
    # 关键：将历史对话 + 当前问题，一起组成新上下文
    context_messages = chat_history + [("user", user_message_2)]
    # 提取消息内容
    context_text = "\n".join([f"{role}: {msg}" for role, msg in context_messages])

    ai_reply_2 = llm.invoke(context_text)
    chat_history.append(("assistant", ai_reply_2))
    print("第二次AI回复：", ai_reply_2)


if __name__ == "__main__":
    main()
