# MCP 基础

学习将 Python 函数暴露成 MCP 工具，再由 LangChain 发现和调用。所有命令在仓库根目录执行。

| ID | 入口 | 运行行为 |
| --- | --- | --- |
| mcp.weather | weather.py | stdio 天气服务，返回模拟数据 |
| mcp.http | Streamable_HTTP_01.py | HTTP 加法服务，地址 http://127.0.0.1:8000/mcp |
| mcp.client | 2_LangChain连接MCP_Server.py | 启动天气子进程、发现工具、通过模型查询 |

~~~powershell
python -m ai_learning run mcp.weather
python -m ai_learning run mcp.http
python -m ai_learning run mcp.client
~~~

前两个服务不需要 API key；运行后会等待 MCP 客户端连接，按 Ctrl+C 结束。stdio 使用标准输入输出传输协议消息，因此不要向服务的 stdout 添加普通打印。HTTP 示例仅监听本机，展示 Streamable HTTP 传输；它返回两个整数相加的结果。

mcp.client 需要 DASHSCOPE_API_KEY，会调用模型服务。它使用当前 Python 解释器和根据自身文件位置计算的服务路径，不需要手动启动天气服务。

1_如何写MCP.py 是最小 stdio 示例。preview.html 是供阅读和自行实验的浏览器工具查看器；浏览器跨域策略或 MCP 服务的 Origin 检查可能限制直接访问，请优先使用 MCP 客户端验证协议。

mcp_proxy.py 是可选的 stdio 转发示例。它将协议消息原样转发，并把副本写入本地 mcp_io.log；日志可能包含工具参数和结果，不应提交到仓库。诊断输出使用 stderr。
