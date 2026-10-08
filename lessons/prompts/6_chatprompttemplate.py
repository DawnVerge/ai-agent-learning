"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from itertools import chain

    from langchain_community.llms.tongyi import Tongyi
    from langchain_core.messages import SystemMessage, HumanMessage
    from langchain_core.prompts import ChatPromptTemplate

    chat_prompt_template = ChatPromptTemplate.from_messages([
        ("system", "假设你是一个{expert}专家"),
        # SystemMessage(content="假设你是一个{expert}专家"),
        ("human", "什么是{user_input}")
        # HumanMessage(content="什么是{user_input}")
    ])
    # prompt = chat_prompt_template.format(expert="AI", user_input="Langgraph")
    # print(type(prompt)) # <class 'str'>
    # print(prompt) # System: 假设你是一个AI专家 Human: 什么是Langgraph

    prompt = chat_prompt_template.invoke(input={"expert": "AI", "user_input": "Langgraph"}).to_string()
    print(type(prompt)) # <class 'str'>
    print(prompt) # System: 假设你是一个AI专家 Human: 什么是Langgraph

    # llm = Tongyi(model=get_chat_model_name('qwen-max'))
    # chain = chat_prompt_template | llm
    # result = chain.stream(input={"expert": "AI", "user_input": "Langgraph"})
    # for chunk in result:
    #     print(chunk, end='', flush=True)


if __name__ == "__main__":
    main()
