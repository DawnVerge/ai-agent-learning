"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.chat_models import ChatTongyi
    from langchain_community.llms.tongyi import Tongyi
    from langchain_core.prompt_values import StringPromptValue, ChatPromptValue
    from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

    # prompt_template = PromptTemplate.from_template(
    #     "你好，我是{name}"
    # )

    # prompt = prompt_template.invoke(input={"name": "阿苑"})
    # # StringPromptValue -> PromptValue
    # print(type(prompt)) # <class 'langchain_core.prompt_values.StringPromptValue'>
    # print(prompt) # text='你好，我是阿苑'
    # print(prompt.text)
    # print(prompt.to_string())

    # prompt_template = ChatPromptTemplate.from_messages([
    #     ("system", "你是谁"),
    #     ("human", "hahah")
    # ])
    #
    # # ChatPromptValue -> PromptValue
    # prompt = prompt_template.invoke(input={})
    # print(type(prompt)) # <class 'langchain_core.prompt_values.ChatPromptValue'>
    # print(prompt) # messages=[SystemMessage(content='你是谁', additional_kwargs={}, response_metadata={}), HumanMessage(content='hahah', additional_kwargs={}, response_metadata={})]
    #



    # Tongyi().invoke()
    # input: LanguageModelInput,
    # LanguageModelInput = PromptValue | str | 消息列表
    # ChatTongyi().invoke()

    # -----------
    # 如果是狭义的llms
    # 1.如果直接invoke/stream调用模型 -》 str
    # 2.LCEL PromptValue
    # --------
    # chat 聊天的模型
    # 1.如果直接invoke/stream调用模型 -》 消息列表
    # 2.LCEL PromptValue
    # ----
    #


if __name__ == "__main__":
    main()
