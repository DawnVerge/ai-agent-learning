# 04 · 历史、会话与文档

`history/` 展示内存消息、会话隔离、文件历史和多轮对话，编号对应 `history.01`–`history.04`。文件历史写入仓库 `.cache/`，不会随代码提交。

`documents/` 展示模型的无状态调用、手动上下文、PDF/Text 加载和向量化，编号对应 `memory.01`–`memory.05`。文档来自仓库自编 `assets/`。

```bash
python -m ai_learning run history.02
python -m ai_learning run memory.04
```

练习：给两个会话传入不同名字，确认历史互不混用；关闭程序后检查内存历史与文件历史的区别。进一步阅读 `projects/lingyu_chat/core/` 的摘要和关键事实管理。
