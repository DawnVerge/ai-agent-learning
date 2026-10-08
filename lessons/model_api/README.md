# 01 · 直接调用模型 API

先运行 `python -m ai_learning run model-api.01`，再按 01–08 观察消息角色、手动历史、系统提示词、流式输出和 token 用量。

所有课例需要 `DASHSCOPE_API_KEY`。`DASHSCOPE_MODEL` 可以覆盖模型名，`OPENAI_BASE_URL` 可以覆盖兼容 API 地址；本课程默认匹配 DashScope。若切换服务商，需同时更换地址、密钥与模型名。

练习：在第 02/03 课比较是否携带前一轮 messages；在第 08 课观察完整回复在流结束后写回历史。不要把“模型记忆”理解成服务端自动保存每次请求。
