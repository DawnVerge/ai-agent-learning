"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.llms.tongyi import Tongyi

    # 1.创建模型的客户端
    llm = Tongyi(model=get_chat_model_name('qwen-max'))

    # 2.调用模型
    user_query_1 = "请简单介绍机器学习"
    user_query_2 = """
    请从以下几个方面介绍机器学习：
    1. 定义（一句话概括）
    2. 三大分类（监督学习、无监督学习、强化学习）
    3. 一个生活化的例子
    4. 与深度学习的区别（用表格呈现）

    要求：语言通俗，适合零基础初学者
    """
    result = llm.stream(input=user_query_2)

    # 3.处理输出
    for chunk in result:
        print(chunk, end='', flush=True)


if __name__ == "__main__":
    main()
