# PDF 文档问答

索引：文件内容 SHA-256 → PyMuPDF 逐页加载 → 中文递归切分 → DashScope 嵌入 → Chroma 持久化。查询：结合历史改写 → 召回 10 条 → LLM 批量重排 → 保留 4 条 → 带来源和页码的回答。最终回答使用原始问题，改写仅用于检索。

从仓库根目录运行：

```console
python -m ai_learning run project.pdf-qa
python -m projects.smart_reading --pdf assets/learning_guide.pdf --question "第二阶段要完成什么？"
python -m projects.smart_reading --interactive
```

需要 `DASHSCOPE_API_KEY`；聊天模型使用仓库统一配置，嵌入模型可用 `DASHSCOPE_EMBEDDING_MODEL` 指定，默认 `text-embedding-v1`。首次问答会调用嵌入 API 并建库，查询改写、重排和回答会调用聊天 API。

默认文档是 `assets/learning_guide.pdf` 中的虚构学习社团手册，所有样本文字均为本项目自编。支持文本型 PDF 和 HTTP(S) PDF URL；本例没有 OCR，扫描件可能提取不到文字。

索引保存在 `.cache/smart_reading/chroma/`。PDF 内容和索引配置相同时复用已完成的索引，跳过解析、切分和嵌入。修改嵌入模型或切分参数后会自动建新索引。首次使用新版缓存时会重建旧索引。远程 PDF 每次检查索引只下载一次。此教学实现没有文档权限控制，也没有大规模并发设计。

`examples/` 是需要 API 的手动演示；`tests/test_rag.py` 使用本地逻辑和替身模型，CI 不调用付费 API。
