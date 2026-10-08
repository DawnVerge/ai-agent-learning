# 数据库 MCP

把 Text-to-SQL 的数据库工具封装为 MCP 服务。client.py 使用当前 Python 解释器启动同目录的 mcp_db_server.py，通过 MCP 发现工具，再交给 LangChain Agent 使用。

| 文件 | 作用 |
| --- | --- |
| client.py | 自然语言查询客户端 |
| mcp_db_server.py | stdio 服务入口 |
| mcp_tools.py | 表名、表结构、只读查询、释放连接池工具和查询提示词 |
| db_manager.py | 环境配置、元数据读取、受限 SQL 与只读事务 |
| mcp_proxy.py | 可选的协议转发和本地日志示例 |

## 准备与运行

按 ../text_to_sql/README.md 手动初始化专用数据库；服务不会自动创建表或写入数据。配置 DASHSCOPE_API_KEY、MYSQL_HOST、MYSQL_PORT、MYSQL_USER、MYSQL_PASSWORD、MYSQL_DATABASE。密码无默认值，数据库配置只在需要时读取，导入模块不会连接数据库。

在仓库根目录执行：

~~~powershell
python -m ai_learning run project.database-mcp
~~~

客户端默认查询销量排名前 5 的商品。它会调用模型 API 和本地数据库，可能产生模型费用。子进程启动路径由 pathlib 推导，不依赖旧机器路径；配置从仓库 .env 或继承的 shell 环境读取。

服务暴露 get_table_names、get_table_schema、execute_sql_query、close_database_connection，以及 sql_assistant prompt。stdio 的 stdout 专供协议使用；不要添加普通启动打印。所有数据库查询采用与 Text-to-SQL 相同的单语句限制、MySQL READ ONLY 事务、回滚和 200 行上限。生产使用仍应配置独立的数据库只读账户。

可选代理的日志会包含协议参数和工具结果，只应保存在本机；日志文件不应提交。离线测试参见 tests/test_database.py，不需要数据库或 API key。
