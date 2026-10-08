# 灵语客服

将意图识别、会话记忆和回答生成组合成电商客服对话。订单查询、改地址、退款等是提示词场景，没有真实电商业务接口。

```bash
python -m ai_learning run project.chat
python -m ai_learning run project.chat -- --message "我想修改收货地址"
```

需要基础依赖和 `DASHSCOPE_API_KEY`。配置 `INTENT_MODEL` 选择意图模型，`DASHSCOPE_MODEL` 选择回答模型。

`chat_service.py` 串联意图识别、低置信度追问、提示词选择、模型回答和记忆更新；`core/` 分别维护历史、摘要和关键事实。记忆保存在进程内，重启后清空。低置信度对话也写入历史，便于理解下一轮补充。

学习任务：观察同一会话中的订单号如何进入关键事实；阅读摘要触发条件；尝试用持久化存储替代内存字典。`examples/` 是需要 API 的手动演示，自动测试不会执行它们。
