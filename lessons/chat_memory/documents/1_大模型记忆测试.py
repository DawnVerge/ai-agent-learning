"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.chat_models import ChatTongyi

    # =========================
    # 演示：大模型的无状态性 (每次调用都是独立的请求)
    # =========================

    # 1. 创建通义千问客户端（选择 qwen3-max 模型）
    llm = ChatTongyi(model=get_chat_model_name('qwen3-max'))

    # 2. 第一次调用：告诉模型用户身份
    user_message = "你好，我是阿苑，是一个AI老师"
    ai_reply = llm.invoke(user_message)
    print("第一次AI回复：", ai_reply)

    # 3. 第二次调用：询问模型“我是谁？”
    # 注意：模型没有记住第一次对话的内容
    user_message = "我是谁？"
    ai_reply_2 = llm.invoke(user_message)
    print("第二次AI回复：", ai_reply_2)


if __name__ == "__main__":
    main()
