# 学习路线

目标是逐步理解模型如何接收消息、如何使用外部知识、如何调用工具，以及如何把这些能力组织成应用。完成某一章的标志是能解释输入、输出与状态如何变化，并能独立改动一个示例。

## 准备

需要 Python 基础，包括函数、类、模块、列表与字典、异常处理。推荐 Python 3.12，环境安装见[首页](../README.md)。

```bash
python -m ai_learning doctor
python -m ai_learning list
python -m ai_learning list --offline
python -m ai_learning run prompts.10
```

`list` 中的 ID 是统一运行入口，文件名中的数字是该主题内的学习顺序。课程中保留了中文文件名，方便对照主题；建议使用 ID 启动。

## 01：模型 API

目录：[lessons/model_api](../lessons/model_api)

学习消息角色、一次请求与多轮请求的差异、历史消息的组织方式、流式响应和 token 用量。模型不会自动保存本地脚本上一次运行的对话，需要应用显式传回历史。

```bash
python -m ai_learning run model-api.01
```

练习：修改系统提示词；比较带历史与不带历史的回答；记录一次请求的输入、输出 token；为交互循环补充退出条件。

需要：基础依赖、`DASHSCOPE_API_KEY` 和可用模型权限。

## 02：LangChain 基础

目录：[lessons/langchain_basics](../lessons/langchain_basics)

对照上一章理解 LLM 与聊天模型、消息对象、`invoke` 与 `stream`，再认识文本如何变成向量。向量相似度是检索信号，需要结合具体任务评估。

练习：用相同问题比较 API 与 LangChain 的调用方式；观察不同消息类型；比较语义相近、关键词相同但语义不同的文本。

需要：基础依赖；涉及模型和 embedding 的示例需要密钥。

## 03：提示词、输出解析与 LCEL

目录：[lessons/prompts](../lessons/prompts)

学习提示词模板、变量替换、少样本示例、消息占位符，以及字符串和 JSON 输出解析。通过手写 `|` 管道理解 LCEL 的组合方式。

```bash
python -m ai_learning run prompts.10
```

练习：给模板新增一个输入变量；增加一条 few-shot 示例；故意让模型输出不合法 JSON 并观察解析错误；为手写管道增加一个处理步骤。

需要：手写 LCEL 示例仅用标准库，其余示例按 `list` 标注准备依赖与密钥。

## 04：会话历史与文档记忆

目录：[history](../lessons/chat_memory/history)、[documents](../lessons/chat_memory/documents)

学习会话 ID、消息历史与文件存储，区分原始历史、摘要和关键事实；认识 TXT/PDF 加载与向量化。文档加载、embedding 和对话历史属于不同的数据处理步骤。

练习：同时维护两个会话并确认历史隔离；重新启动脚本检查文件历史；比较完整历史与摘要的长度及信息损失；打印文档页码等元数据。

需要：基础依赖；文档加载安装 `.[rag]`；涉及模型的示例需要密钥。

## 05：RAG 基础

目录：[lessons/rag_basics](../lessons/rag_basics)

按 Document → 加载 → 切分 → embedding → Chroma → 检索的顺序理解链路，再观察 MMR 如何影响返回片段的多样性。仓库含一个 Chroma Notebook，可在安装 Jupyter 后交互阅读；统一运行器以 Python 示例为主。

练习：固定同一文档与问题，改变 chunk size、overlap 和召回数量；打印片段与元数据；比较相似度检索和 MMR 的结果。

需要：`.[rag]`；加载、切分等离线示例无需密钥，在线 embedding 需要密钥。网页加载仍会访问网络，即使不调用模型也不属于离线示例。

## 06：混合检索

目录：[lessons/hybrid_search](../lessons/hybrid_search)

理解欧氏距离、余弦相似度、BM25 与中文分词，再学习向量召回与关键词召回如何经 RRF 融合。不同检索方法的原始分数不一定能直接相加。

练习：准备包含专有名词、同义表达和精确编号的问题；分别查看 BM25、向量和融合排序；分析每种方式遗漏的片段。

需要：`.[rag]`；涉及 DashScope embedding 的示例需要密钥。

## 07：Agent 与工具调用

目录：[lessons/agents](../lessons/agents)

学习工具的类型标注、描述、参数与返回值，先手动处理工具调用，再使用 LangChain v1 的 `create_agent`。观察工具错误如何进入 `ToolMessage`，以及重试何时会增加请求次数。

练习：增加一个只读工具；区分模型提出调用与程序真正执行调用；让工具返回可预期错误；为重试设置上限。

需要：基础依赖、模型密钥，以及支持工具调用的模型。演示天气、库存等结果可能为模拟值。

## 08：MCP

目录：[lessons/mcp](../lessons/mcp)

学习把工具从 Agent 脚本拆成独立服务，了解 stdio 与 Streamable HTTP 的连接方式，使用客户端发现工具并转为 LangChain 工具。

练习：启动本地模拟天气服务；查看工具描述和参数 schema；添加一个简单计算工具；解释 stdio 为什么不能混入普通 `stdout` 日志。

需要：`.[mcp]`；本地模拟服务自身无需密钥，连接模型 Agent 的客户端需要密钥。HTTP 示例是本地教学服务。

## 综合实战

| 项目 | 先修章节 | 建议观察的问题 |
| --- | --- | --- |
| [灵语客服](../projects/lingyu_chat) | 01–04 | 意图识别如何决定提示词？摘要与关键事实如何进入上下文？ |
| [PDF 智能阅读](../projects/smart_reading) | 01–06 | 改写前后召回是否变化？重排保留了哪些片段？页码来自哪里？ |
| [Text-to-SQL](../projects/text_to_sql) | 01、02、07 | Agent 先查询结构还是直接生成 SQL？生成结果是否符合实际 schema？ |
| [数据库 MCP](../projects/database_mcp) | 07、08 与 MySQL 基础 | 客户端如何发现数据库工具？哪些能力属于服务端？ |

```bash
python -m ai_learning run project.chat
python -m ai_learning run project.pdf-qa -- --question "这份文档介绍了什么？"
python -m ai_learning run project.text-to-sql
python -m ai_learning run project.database-mcp
```

数据库项目先准备独立测试库与 `MYSQL_*` 环境变量；[初始化 SQL](../projects/text_to_sql/db_init.sql) 包含练习用商品和订单数据。不要把个人文档、业务数据或对话记录提交到仓库。

## 如何确认自己学会了

每完成一个主题，尝试画出数据流，解释每一步的输入与输出，独立改变一个参数，再记录变化。对 RAG 和 Agent，保存少量可复现的问题与预期行为，比只观察一次“回答看起来不错”更有帮助。

```bash
python -m ai_learning check
python -m unittest discover -s tests -v
```

自动检查验证仓库与离线行为；真实服务的效果、费用、权限与连接情况需要另外验证。
