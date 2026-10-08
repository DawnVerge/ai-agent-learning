"""独立教学示例；通过 python -m ai_learning run <id> 运行。"""

def main():
    import os
    from ai_learning.config import PROJECT_ROOT, get_api_key, get_chat_model_name

    # ========== 模拟提示词模板 ==========
    class PromptTemplate:
        def __init__(self, template):
            self.template = template

        def __or__(self, next_component):
            # 返回一个 RunnableSequence 对象
            return RunnableSequence(self, next_component)

        def invoke(self, input_data):
            # 将模板中的占位符替换为实际值
            result = self.template.format(**input_data)
            print(f"[PromptTemplate] 输出: {result}")
            return result


    # ========== 模拟模型 ==========
    class Model:
        def __init__(self, name="ChatTongyi"):
            self.name = name

        def __or__(self, next_component):
            return RunnableSequence(self, next_component)

        def invoke(self, input_text):
            # 模拟模型生成回复
            if "你好" in input_text:
                result = f"AI回复：你好！很高兴见到你。"
            elif "名字" in input_text:
                result = f"AI回复：你的名字是阿苑。"
            else:
                result = f"AI回复：收到你的问题：{input_text}"
            print(f"[Model] 输出: {result}")
            return result


    # ========== 模拟输出解析器 ==========
    class StrOutputParser:
        def __or__(self, next_component):
            return RunnableSequence(self, next_component)

        def invoke(self, input_data):
            # 如果输入是 AIMessage 对象，提取 content；否则直接返回
            if hasattr(input_data, 'content'):
                result = input_data.content
            else:
                result = input_data
            print(f"[StrOutputParser] 输出: {result}")
            return result


    # ========== 序列执行器 ==========
    class RunnableSequence:
        def __init__(self, first, second):
            self.first = first
            self.second = second

        def __or__(self, next_component):
            # 支持继续串联
            return RunnableSequence(self, next_component)

        def invoke(self, input_data):
            # 依次执行：first → second
            intermediate = self.first.invoke(input_data)
            return self.second.invoke(intermediate)


    # ========== 测试三个 | 串联 ==========
    print("=== 模拟 PromptTemplate | Model | StrOutputParser ===\n")

    # 1. 创建组件
    prompt = PromptTemplate(template="用户说：{user_input}，请回复")
    model = Model()
    parser = StrOutputParser()

    # 2. 使用三个 | 串联
    chain = prompt | model | parser

    # 3. 执行
    result = chain.invoke({"user_input": "你好"})

    print(f"\n最终结果: {result}")
    print(f"结果类型: {type(result)}")


if __name__ == "__main__":
    main()
