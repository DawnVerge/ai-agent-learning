# AI Agent Learning

**从第一次模型调用，到 RAG、工具调用和 MCP：一套以 Python 代码为主线的中文 AI 应用学习项目。**

[English](README.en.md) · [学习路线](docs/learning-path.md) · [依赖说明](docs/dependencies.md) · [贡献指南](CONTRIBUTING.md)

[![Offline checks](https://github.com/DawnVerge/ai-agent-learning/actions/workflows/ci.yml/badge.svg)](https://github.com/DawnVerge/ai-agent-learning/actions/workflows/ci.yml)

本项目适合掌握 Python 基础、希望动手理解大模型应用的学习者。课程保留按编号递进的示例，每个主题先拆解一个概念，再通过客服、PDF 问答和数据库 Agent 把它们串起来。默认使用通义千问与 DashScope，模型调用同时覆盖 OpenAI 兼容 SDK 和 LangChain。

维护者：[DawnVerge](https://github.com/DawnVerge) · Python 3.11+，推荐 3.12 · LangChain v1 · MIT

## 快速开始

克隆项目后，在项目根目录执行以下命令。

### Windows / PowerShell

```powershell
git clone https://github.com/DawnVerge/ai-agent-learning.git
cd ai-agent-learning
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[all,dev]"
Copy-Item .env.example .env
python -m ai_learning doctor
python -m ai_learning list --offline
python -m ai_learning run prompts.10
```

若 PowerShell 阻止激活脚本，可以直接使用 `.\.venv\Scripts\python.exe` 代替后续命令中的 `python`。

### macOS / Linux / Bash

```bash
git clone https://github.com/DawnVerge/ai-agent-learning.git
cd ai-agent-learning
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[all,dev]'
cp .env.example .env
python -m ai_learning doctor
python -m ai_learning list --offline
python -m ai_learning run prompts.10
```

`prompts.10` 是手写 LCEL 的离线演示，运行它不需要模型密钥，也不调用外部服务。想先轻量安装，可用 `python -m pip install -e .`；后续按主题安装 `.[rag]`、`.[mcp]` 或 `.[sql]`，详见[依赖说明](docs/dependencies.md)。

### 第一次在线模型调用

编辑 `.env`，填写自己的密钥：

```dotenv
DASHSCOPE_API_KEY=your-api-key
DASHSCOPE_MODEL=qwen3-max
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

然后运行：

```bash
python -m ai_learning run model-api.01
```

在线模型、embedding 和重排会访问外部服务，可能产生账号费用。请在服务商控制台确认模型权限、地域、额度和计费；运行 PDF 问答前确认文档内容可以发送给所用模型服务。

## 统一学习入口

```bash
python -m ai_learning list
python -m ai_learning list --offline
python -m ai_learning run prompts.10
python -m ai_learning doctor
python -m ai_learning check
```

`list` 展示课程与项目 ID；`--offline` 只显示可离线运行的条目。`run` 根据 ID 启动对应文件，入口参数放在 `--` 后。`doctor` 检查本机环境；`check` 检查 Python 语法、课程目录、密钥和旧机器路径等静态问题。

## 课程地图

| 顺序 | 目录 | 学习内容 |
| --- | --- | --- |
| 01 | [model_api](lessons/model_api) | API 调用、消息角色、多轮对话、流式输出、token 用量 |
| 02 | [langchain_basics](lessons/langchain_basics) | LLM 与聊天模型、消息类型、embedding、相似度 |
| 03 | [prompts](lessons/prompts) | 提示词模板、少样本、上下文、输出解析、手写 LCEL |
| 04 | [chat_memory](lessons/chat_memory) | 会话隔离、文件历史、文档加载与向量化 |
| 05 | [rag_basics](lessons/rag_basics) | Document、切分与 overlap、Chroma、MMR |
| 06 | [hybrid_search](lessons/hybrid_search) | 欧氏距离、余弦相似度、BM25、混合检索与 RRF |
| 07 | [agents](lessons/agents) | 工具定义、工具调用、create_agent、多工具、异常与重试 |
| 08 | [mcp](lessons/mcp) | MCP 服务、stdio、Streamable HTTP、LangChain 客户端 |

建议按顺序学习，也可以从 `list --offline` 选择无需密钥的示例。详细目标、练习和先修关系见[学习路线](docs/learning-path.md)。

## 四个实战项目

| 项目 | 运行入口 | 串联的能力 |
| --- | --- | --- |
| [灵语客服](projects/lingyu_chat) | `python -m ai_learning run project.chat` | 意图识别、提示词路由、会话历史、摘要和关键事实 |
| [PDF 智能阅读](projects/smart_reading) | `python -m ai_learning run project.pdf-qa -- --question "这份文档介绍了什么？"` | 文档索引、问题改写、召回、模型重排、带页码的回答 |
| [Text-to-SQL](projects/text_to_sql) | `python -m ai_learning run project.text-to-sql` | 数据库结构查询、SQL 工具、自然语言查询 |
| [数据库 MCP](projects/database_mcp) | `python -m ai_learning run project.database-mcp` | 将数据库能力封装为 MCP 工具并交给 Agent 调用 |

PDF 入口默认使用仓库样本文档；替换文档和项目参数请查看对应入口的帮助。数据库项目需要自行启动 MySQL，并在 `.env` 配置 `MYSQL_HOST`、`MYSQL_PORT`、`MYSQL_USER`、`MYSQL_PASSWORD` 和 `MYSQL_DATABASE`。可将 [db_init.sql](projects/text_to_sql/db_init.sql) 导入专用练习数据库。

这些项目是学习示例。天气、库存等演示工具可能返回固定模拟值；示例商品和订单数据用于练习，不代表真实业务。模型生成的 SQL 和回答需要核验，数据库练习请使用测试数据与最小权限账号。PDF 页码引用用于定位来源，不代表结论已经得到验证。

## 目录结构

```text
ai-agent-learning/
├── ai_learning/          # 课程目录、运行器和环境检查
├── lessons/              # 按主题递进的独立示例
│   ├── model_api/
│   ├── langchain_basics/
│   ├── prompts/
│   ├── chat_memory/
│   │   ├── history/
│   │   └── documents/
│   ├── rag_basics/
│   ├── hybrid_search/
│   ├── agents/
│   └── mcp/
├── projects/             # 四个综合实战
│   ├── lingyu_chat/
│   ├── smart_reading/
│   ├── text_to_sql/
│   └── database_mcp/
├── assets/               # 可公开的学习样本
├── docs/                 # 学习、依赖和发布说明
├── tests/                # 无需密钥的自动化检查
├── .env.example          # 环境变量模板
└── pyproject.toml        # 安装与可选依赖
```

## 本地验证与贡献

```bash
python -m ai_learning check
python -m unittest discover -s tests -v
```

上述检查可以离线执行，不会验证真实模型响应或 MySQL 连接。项目内 `test/` 与课件中的 `test.py` 多为学习演示；统一自动化测试位于根目录 `tests/`。

欢迎修复示例、补充解释和提出新的练习。提交前请阅读[贡献指南](CONTRIBUTING.md)，不要提交 `.env`、API 密钥、数据库密码、私人文档、会话记录或本机虚拟环境。安全问题请参阅[安全说明](SECURITY.md)。

## 许可证

代码以 [MIT License](LICENSE) 开源。外部模型服务、依赖库和自行加入的学习材料遵循各自的使用条款与许可证。
