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
    result = llm.invoke(input="你是谁？")

    # 3.处理输出
    print(type(result)) # <class 'str'>
    print(result) # 我是Qwen，由阿里云开发的超大规模语言模型。我的目标是...


if __name__ == "__main__":
    main()
