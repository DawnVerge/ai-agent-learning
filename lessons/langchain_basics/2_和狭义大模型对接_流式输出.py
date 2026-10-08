"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.llms.tongyi import Tongyi

    # 1.创建模型的客户端
    # 之前我们使用的是 qwen3-max,但是qwen3-max是聊天模型，不是狭义的llms
    # qwen-max 是狭义的llms，适合于单次调用
    llm = Tongyi(model=get_chat_model_name('qwen-max'))

    # 2.调用模型
    result = llm.stream(input="你是谁？")

    # 3.处理输出
    for chunk in result:
        print(chunk)
        # print(chunk, end='', flush=True)


if __name__ == "__main__":
    main()
