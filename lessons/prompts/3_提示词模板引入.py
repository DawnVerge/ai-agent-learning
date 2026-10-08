"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.llms.tongyi import Tongyi
    from langchain_core.prompts import PromptTemplate

    # 1.创建模型的客户端
    llm = Tongyi(model=get_chat_model_name('qwen-max'))

    # 2.调用模型
    # 2.1. 准备提示词模板
    prompt_template = PromptTemplate.from_template(
        "假设你是一个{expert}专家，请你解释一下{content}是什么。"
    )
    # 2.2. 替换占位符
    prompt = prompt_template.format(expert="AI", content="Langgraph")
    # prompt = prompt_template.invoke(input={"expert": "AI", "content": "Langgraph"}).to_string()
    print(type(prompt))  # <class 'str'>
    print(prompt)
    # 2.3 调用模型
    result = llm.stream(input=prompt)

    # 3.处理输出
    for chunk in result:
        print(chunk, end='', flush=True)


if __name__ == "__main__":
    main()
