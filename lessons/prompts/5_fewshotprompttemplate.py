"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    from langchain_community.llms.tongyi import Tongyi
    from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

    # 第一步：定义示例
    examples = [
        {"input": "高兴", "output": "愉悦"},
        {"input": "快速", "output": "迅猛"},
        {"input": "美丽", "output": "绚丽"}
    ]

    # 第二步：定义示例格式化模板
    example_prompt = PromptTemplate.from_template(
        template="输入：{input}\n输出：{output}"
    )
    # 第三步：创建 FewShotPromptTemplate
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="请根据以下示例，将输入词语转换为同义词",
        suffix="基于示例回答问题。用户输入：{word}\n输出：",
        input_variables=["word"]
    )

    # 第四步：调用
    # prompt_text = few_shot_prompt.format(word="悲伤")
    prompt_text = few_shot_prompt.invoke(input={"word": "悲伤"})
    print(type(prompt_text))
    print(prompt_text)
    # llm = Tongyi(model=get_chat_model_name('qwen-max'))
    # chain = few_shot_prompt | llm
    # print(chain.invoke({"word": "悲伤"}))


if __name__ == "__main__":
    main()
