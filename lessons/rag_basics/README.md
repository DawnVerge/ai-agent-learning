# RAG 基础

按原教学编号学习 Document、加载器、文本切分、嵌入、Chroma 与 MMR。编号 5 补充字符分割器，与编号 6 的递归切分进行比较。编号 12 已转为普通 Python 脚本，避免携带旧 Notebook 输出。

示例命令：`python -m ai_learning run rag.02`。01-03、05-08 无需 API 密钥；04 需要联网访问官方文档；09-14 需要 `DASHSCOPE_API_KEY`，会调用嵌入 API。Chroma 演示数据保存到仓库 `.cache/rag_basics/`。

所有文档使用 `assets/` 中的自编教学样本。先比较切分结果，再观察语义排序与 MMR 对结果的影响。
