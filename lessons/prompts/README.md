# 03 · 提示词与输出解析

01–04 逐步构建提示词与 LCEL；05–07 展示少样本、聊天模板与历史占位符；08–09 解析字符串和 JSON；10 用纯 Python 演示 `prompt | model | parser` 的执行原理。

```bash
python -m ai_learning run prompts.10
python -m ai_learning run prompts.05
```

第 10 课仅需 Python，05–07 需安装基础依赖但不调用模型 API；其余在线课例需要密钥。

练习：在第 10 课添加一个输出转换组件，观察 `__or__` 如何组装调用链；在第 09 课改变 JSON 格式要求，比较结构化结果与字符串结果。
