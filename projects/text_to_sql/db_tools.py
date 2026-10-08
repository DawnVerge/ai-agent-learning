"""自然语言 → 数据库结构 → 只读 SQL → 中文回答。"""

import os

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

from ai_learning.config import get_api_key
from db_manager import DBManager


SYSTEM_PROMPT = """你是数据库查询助手。
先查看表名和表结构，再根据真实字段编写一条 SELECT 查询。
只能读取数据，不能修改数据或执行多条语句。
涉及多个表时按结构使用 JOIN，默认限制结果数量。
查询失败时说明原因，不要编造结果。用中文解释查询结果。
"""


def create_tools(db: DBManager):
    @tool
    def get_table_names() -> str:
        """列出已配置数据库中的表。"""
        return ", ".join(db.get_table_names()) or "数据库中没有表。"

    @tool
    def get_table_schema() -> str:
        """读取所有表的字段、注释、主键和索引。"""
        return str(db.get_all_table_schemas())

    @tool
    def execute_sql_query(sql: str) -> str:
        """执行一条只读 SELECT 查询，最多返回 200 行。"""
        try:
            rows = db.execute_query(sql)
            return str(rows) if rows else "查询结果为空。"
        except Exception:
            return "查询未完成。请检查只读 SQL、表结构和数据库配置，不要编造结果。"

    return [get_table_names, get_table_schema, execute_sql_query]


def main():
    get_api_key()
    db = DBManager.from_env()
    agent = create_agent(
        model=ChatTongyi(model=os.getenv("DASHSCOPE_MODEL", "qwen3-max")),
        tools=create_tools(db),
        system_prompt=SYSTEM_PROMPT,
    )
    try:
        question = "销量排名前 5 的商品是哪些？"
        print(f"用户：{question}")
        result = agent.invoke({"messages": [("user", question)]})
        print(result["messages"][-1].content)
    finally:
        db.close()


if __name__ == "__main__":
    main()
