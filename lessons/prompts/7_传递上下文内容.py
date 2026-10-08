"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.chat_models import ChatTongyi
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    chat_prompt_template = ChatPromptTemplate.from_messages([
        ("system", "假设你是一个AI专家"),
        MessagesPlaceholder("history"),
        ("human", "我刚才问了什么内容？"),
    ])

    chat_history = [
        ("human", "什么是Langgraph"),
        ("ai", "这是一条用于演示历史消息占位符的示例回答。")
    ]

    # text = chat_prompt_template.format(history=chat_history)
    # print(type(text))
    # print(text)
    print(chat_prompt_template.invoke(input={"history": chat_history}).to_string())

    # llm = ChatTongyi(model=get_chat_model_name('qwen3-max'))
    # chain = chat_prompt_template | llm
    # result = chain.invoke(input={"history": chat_history})
    #
    # print(type(result)) # <class 'langchain_core.messages.ai.AIMessage'>
    # print(result) # content='你刚才问的是：“什么是Langgraph”。' additional_kwargs={} res
    # print(result.content) # 你刚才问的是：“什么是Langgraph”。


if __name__ == "__main__":
    main()
