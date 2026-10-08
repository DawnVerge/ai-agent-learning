# 02 · LangChain 基础

运行 `python -m ai_learning run langchain.01`，按 01–08 了解 LLM 与 ChatModel、消息对象、多轮历史、embedding 和向量相似度。

本组示例会调用模型服务，需要基础依赖与 `DASHSCOPE_API_KEY`。学习重点是对照上一组直接 API 调用，观察框架怎样组织消息与输出。

练习：将相同的用户输入分别传给 LLM 与 ChatModel；修改第 08 课的两段文本，观察向量距离怎样变化。相似度用于检索排序，不等于事实正确性。
