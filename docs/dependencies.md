# 环境与依赖

推荐使用 Python 3.12，项目面向 Python 3.11 及以上。请为项目创建独立 `.venv`，不要复用其他 LangChain 项目的环境。实际安装范围以根目录 [pyproject.toml](../pyproject.toml) 为准。

## 按需安装

| 命令 | 用途 |
| --- | --- |
| `python -m pip install -e .` | 模型 API、LangChain 基础、提示词、会话历史与基本 Agent |
| `python -m pip install -e '.[rag]'` | PDF/网页加载、文本切分、Chroma 与混合检索 |
| `python -m pip install -e '.[mcp]'` | MCP 服务与 LangChain MCP 客户端 |
| `python -m pip install -e '.[sql]'` | SQLAlchemy 与 MySQL 驱动 |
| `python -m pip install -e '.[all,dev]'` | 全部学习依赖和开发工具 |

PowerShell 可以将上表中的单引号写成双引号。`-e` 表示可编辑安装：修改仓库源码后无需重新安装。首次安装需要访问包索引；离线运行表示示例运行时不访问外部服务。

## 为什么选择这些兼容线

本项目代码使用 `from langchain.agents import create_agent`、`langchain.messages` 和 Agent middleware，因此以 **LangChain v1** 为统一接口。不能将 `langchain` 降到 0.3 后继续使用这些入口。传统 LCEL、消息、提示词与解析器继续从 `langchain_core` 导入。[LangChain v1 官方迁移指南](https://docs.langchain.com/oss/python/migrate/langchain-v1)

`ChatTongyi` 和 `DashScopeEmbeddings` 来自 `langchain-community`，还需要单独安装 `dashscope`。`ChatTongyi` 官方源码读取 `DASHSCOPE_API_KEY` 并实现 `bind_tools`，因此基本对话与工具调用可以保留这一接入方式。[ChatTongyi 官方源码](https://github.com/langchain-ai/langchain-community/blob/main/libs/community/langchain_community/chat_models/tongyi.py)、[DashScope PyPI](https://pypi.org/project/dashscope/)

Chroma 使用独立集成包 `langchain-chroma`；文本切分使用 `langchain-text-splitters`。这些集成与 LangChain v1 的 `langchain-core` 兼容；不需要另行固定一个旧版本的 `chromadb`。[langchain-chroma PyPI](https://pypi.org/project/langchain-chroma/)、[langchain-text-splitters PyPI](https://pypi.org/project/langchain-text-splitters/)

MCP 示例使用 **SDK v1 的 FastMCP 接口**：`from mcp.server.fastmcp import FastMCP`。SDK v2 移除了该导入路径，所以依赖必须保持 `mcp<2`。`langchain-mcp-adapters` 0.3.2 同样声明 `mcp>=1.24,<2`，本项目沿用这条兼容线。升级到 MCP v2 需要同时迁移服务端和客户端。[MCP 官方迁移说明](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/migration.md)、[适配器官方依赖声明](https://github.com/langchain-ai/langchain-mcp-adapters/blob/main/pyproject.toml)

## 包与用途

| 包 | 用途 |
| --- | --- |
| `openai` | 调用 DashScope 的 OpenAI 兼容接口 |
| `langchain`、`langchain-core` | Agent、消息、提示词、Runnable 和输出解析 |
| `langchain-community`、`dashscope` | 通义聊天模型、embedding、文档加载与历史存储 |
| `numpy`、`rank-bm25`、`jieba` | 向量计算、BM25、中文分词 |
| `PyMuPDF` | PDF 加载器的实际解析后端 |
| `beautifulsoup4`、`requests` | 网页解析与 HTTP 获取 |
| `langchain-chroma`、`langchain-text-splitters` | 向量存储与文档切分 |
| `mcp`、`langchain-mcp-adapters` | MCP 服务、连接与工具转换 |
| `SQLAlchemy`、`PyMySQL` | 数据库访问与 `mysql+pymysql` 驱动 |
| `pydantic` | 结构化输出的 schema |

`PyMySQL` 与 `beautifulsoup4` 可能不会直接出现在示例的 `import` 中，但相应驱动或加载器运行时仍需要它们。Jupyter Notebook 是补充学习材料；需要交互运行时自行安装 Jupyter。

## 配置与自检

```bash
python -m ai_learning doctor
python -m pip check
python -m ai_learning check
python -m unittest discover -s tests -v
```

`doctor` 检查环境准备情况，`pip check` 检查已安装包的依赖约束。后两项用于离线验证仓库，不会自动调用模型、下载远程文档或连接 MySQL。

环境变量模板见 [.env.example](../.env.example)。项目使用标准库读取 `.env` 的 `KEY=value` 配置，保留已设置的 shell 环境变量，不执行命令或变量插值。在线示例需要 `DASHSCOPE_API_KEY`；默认模型由 `DASHSCOPE_MODEL` 控制。`OPENAI_BASE_URL` 用于 OpenAI 兼容 SDK 的地址配置，`ChatTongyi` 使用 DashScope SDK，不会自动跟随此变量切换服务商。

若出现 `cannot import create_agent`，先检查是否误装 LangChain 0.3；若出现 `No module named mcp.server.fastmcp`，检查是否误装 MCP 2.x。遇到依赖冲突时，优先创建新的虚拟环境并按 `pyproject.toml` 重装，再报告 Python 版本、安装命令和经过脱敏的错误。

依赖说明依据 2026-10-08 查阅的官方 PyPI 元数据与项目文档。版本范围用于维持接口兼容；真实服务权限与模型效果需要单独验证。
