# Agent 基础

通过七个小脚本理解模型工具调用与 Agent 的区别。运行命令均在仓库根目录执行；先按根 README 安装依赖，并在本机环境或不提交的 .env 中配置 DASHSCOPE_API_KEY。DASHSCOPE_MODEL 可选，默认 qwen3-max。

| ID | 内容 | 观察重点 |
| --- | --- | --- |
| agents.01 | LLM 的局限 | 没有实时工具时，模型如何处理天气问题 |
| agents.02 | 给模型添加工具 | 手动执行工具，并通过 ToolMessage 反馈 |
| agents.03 | 提供多个工具 | 观察同一响应中的多个工具请求 |
| agents.04 | 创建 Agent | create_agent 自动协调工具调用 |
| agents.05 | 异常处理 | 工具异常转为模型可理解的消息 |
| agents.06 | 重试逻辑 | 最多三次尝试；北京示例会持续失败 |
| agents.07 | 多步工具调用 | 商品名称 → 商品 ID → 商品价格 |

~~~powershell
python -m ai_learning run agents.01
python -m ai_learning run agents.02
python -m ai_learning run agents.07
~~~

这些脚本会调用模型服务，可能产生费用。天气、景点与商品信息都是明确标注的静态示例。第 3 课只打印工具请求；第 4 课开始交由 Agent 执行工具。所有执行放在 main 入口，导入文件不会发起模型请求。
