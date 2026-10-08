# 距离与混合检索

01 与 03 使用小向量，直接运行且无需密钥。02 与 04 将同一批自编文档存入 Chroma，比较 l2 和 cosine 的距离分数；05 观察相近型号的语义检索结果；06 用 jieba、BM25 和 RRF 融合检索排名。02、04、05、06 需要 `DASHSCOPE_API_KEY`。

运行示例：`python -m ai_learning run hybrid.06`。样本文档位于 `assets/retrieval_documents.json`，设备与数值均为虚构。RRF 依据排名计算分数，不将量纲不同的 BM25 分数和余弦相似度直接相加。
