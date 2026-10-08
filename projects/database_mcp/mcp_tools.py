"""将 MySQL 元数据读取和只读查询注册为 MCP 工具。"""

from mcp.server.fastmcp import FastMCP

from db_manager import DBManager


mcp = FastMCP("database")
_db = None


def get_database() -> DBManager:
    """第一次调用工具时才读取数据库配置；不会在导入时连接。"""
    global _db
    if _db is None:
        _db = DBManager.from_env()
    return _db


@mcp.tool()
def get_table_names() -> str:
    """列出已配置数据库中的所有表。"""
    return ", ".join(get_database().get_table_names()) or "数据库中没有表。"


@mcp.tool()
def get_table_schema() -> str:
    """读取所有表的字段、注释、主键和索引。"""
    return str(get_database().get_all_table_schemas())


@mcp.tool()
def execute_sql_query(sql: str) -> str:
    """执行一条只读 SELECT 查询，最多返回 200 行。"""
    try:
        rows = get_database().execute_query(sql)
        return str(rows) if rows else "查询结果为空。"
    except Exception:
        return "查询未完成。请检查只读 SQL、表结构和数据库配置，不要编造结果。"


@mcp.tool()
def close_database_connection() -> str:
    """释放当前数据库连接池；下次调用可重新创建。"""
    global _db
    if _db is not None:
        _db.close()
        _db = None
    return "数据库连接池已释放。"


@mcp.prompt()
def sql_assistant() -> str:
    """查询助手的工作流程。"""
    return (
        "先调用 get_table_names 和 get_table_schema，再编写一条 SELECT 查询。"
        "只能读取数据，不能修改数据。限制结果数量，用中文解释真实结果。"
        "查询失败时说明失败，不要编造数据。"
    )
