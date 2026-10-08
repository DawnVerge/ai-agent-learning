"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from openai import OpenAI

    # 1.创建客户端对象
    client = OpenAI(api_key=get_api_key(),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    )

    # 2. 第一次调用：告诉模型用户身份
    completion = client.chat.completions.create(
        model=get_chat_model_name('qwen3-max'),
        messages=[
            {"role": "user", "content": "你好，我是阿苑，是一个AI老师。"},
        ]
    )
    print(completion.model_dump_json())

    # 3. 第二次调用：询问模型“我是谁？”
    completion = client.chat.completions.create(
        model=get_chat_model_name('qwen3-max'),
        messages=[
            {"role": "user", "content": "我是谁？"},
        ]
    )
    print(completion.model_dump_json())
    # print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
