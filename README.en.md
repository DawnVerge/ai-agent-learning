# AI Agent Learning

**Learn AI application development in Python, from the first model call to RAG, tool calling, and MCP.**

[中文](README.md) · [Learning path](docs/learning-path.md) · [Dependencies](docs/dependencies.md) · [Contributing](CONTRIBUTING.md)

This repository is a code-first learning resource for developers with basic Python knowledge. Numbered examples introduce one concept at a time, while four projects connect those concepts into complete workflows. The lessons and comments are primarily in Chinese. The default provider is Qwen through DashScope, using both the OpenAI-compatible SDK and LangChain.

Maintainer: [DawnVerge](https://github.com/DawnVerge) · Python 3.11+, recommended 3.12 · LangChain v1 · MIT

## Quick start

Clone the repository, then run these commands from its root directory.

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

If script activation is blocked, use `.\.venv\Scripts\python.exe` instead of `python` in the remaining commands.

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

`prompts.10` demonstrates a handwritten LCEL-style pipeline without third-party packages, API keys, or external calls. A smaller install is available with `python -m pip install -e .`; add `.[rag]`, `.[mcp]`, or `.[sql]` when needed.

To make an online model call, edit `.env`:

```dotenv
DASHSCOPE_API_KEY=your-api-key
DASHSCOPE_MODEL=qwen3-max
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

```bash
python -m ai_learning run model-api.01
```

Online chat, embeddings, and model-based reranking use external services and may incur charges. Check provider access, region, quotas, and pricing. Only use documents you are permitted to send to the selected model service.

## Lessons and commands

| Directory | Topics |
| --- | --- |
| [model_api](lessons/model_api) | API calls, roles, conversation history, streaming, token usage |
| [langchain_basics](lessons/langchain_basics) | LLMs, chat models, messages, embeddings, similarity |
| [prompts](lessons/prompts) | Templates, few-shot prompts, context, parsers, LCEL |
| [chat_memory](lessons/chat_memory) | Session isolation, file history, document loading |
| [rag_basics](lessons/rag_basics) | Documents, splitting, Chroma, MMR |
| [hybrid_search](lessons/hybrid_search) | Distances, BM25, hybrid retrieval, RRF |
| [agents](lessons/agents) | Tools, create_agent, errors, retries |
| [mcp](lessons/mcp) | MCP servers, stdio, Streamable HTTP, clients |

```bash
python -m ai_learning list                 # Discover IDs and requirements
python -m ai_learning list --offline       # Entries without external calls
python -m ai_learning run prompts.10       # Run an entry
python -m ai_learning doctor               # Inspect the local environment
python -m ai_learning check                # Static repository checks
```

Pass entry-specific arguments after `--`. See the [learning path](docs/learning-path.md) for suggested exercises and prerequisites.

## Projects

| Project | Entry ID | What it demonstrates |
| --- | --- | --- |
| [Lingyu chat](projects/lingyu_chat) | `project.chat` | Intent routing, conversation history, summaries, facts |
| [PDF question answering](projects/smart_reading) | `project.pdf-qa` | Indexing, query rewriting, retrieval, reranking, page references |
| [Text-to-SQL](projects/text_to_sql) | `project.text-to-sql` | Database schemas, SQL tools, natural-language queries |
| [Database MCP](projects/database_mcp) | `project.database-mcp` | Exposing database tools through MCP |

```bash
python -m ai_learning run project.chat
python -m ai_learning run project.pdf-qa -- --question "What does this document explain?"
python -m ai_learning run project.text-to-sql
python -m ai_learning run project.database-mcp
```

PDF QA uses the included sample by default. MySQL projects require a running server and `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` in `.env`. Import [db_init.sql](projects/text_to_sql/db_init.sql) into a dedicated practice database if you need sample data.

These are educational examples. Some weather and inventory tools return fixed mock values; product and order records are practice data. Review model-generated SQL and answers, and use a test database with limited permissions. Page references help locate evidence but do not establish answer correctness.

## Repository layout

```text
ai_learning/   Catalog, runner, and checks
lessons/       Numbered lessons grouped by topic
projects/      Four integrated applications
assets/        Public learning samples
docs/          Learning, dependency, and publishing guides
tests/         Offline automated tests
```

## Validation and contributions

```bash
python -m ai_learning check
python -m unittest discover -s tests -v
```

These checks do not call a live model or validate a MySQL connection. The automated suite is in the root `tests/` directory; lesson `test.py` files and project `test/` directories contain learning demonstrations.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not commit keys, passwords, private documents, conversations, virtual environments, or `.env` files.

## License

The code is available under the [MIT License](LICENSE). Dependencies, provider services, and additional learning materials retain their own licenses and terms.
