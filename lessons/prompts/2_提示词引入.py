"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.llms.tongyi import Tongyi

    # 1.创建模型的客户端
    llm = Tongyi(model=get_chat_model_name('qwen-max'))

    # 2.调用模型
    # 2.1. 用户直接提问
    # user_query = "假设你是一个AI专家，请你解释一下Langchain是什么。"
    # 2.2. 支持占位符注入
    user_query = "假设你是一个{expert}专家，请你解释一下{content}是什么。".format(expert="AI", content="Langgraph")

    result = llm.stream(input=user_query)

    # 3.处理输出
    for chunk in result:
        print(chunk, end='', flush=True)


if __name__ == "__main__":
    main()
