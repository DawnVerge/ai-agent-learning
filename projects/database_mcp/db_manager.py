"""MySQL 元数据读取和受限的只读查询；创建实例不会连接数据库。"""

import re
from typing import Any

from sqlalchemy import URL, create_engine, inspect, text


_TOKEN = re.compile(
    r"(?P<space>\s+)"
    r"|(?P<line>--(?=\s)[^\r\n]*|\#[^\r\n]*)"
    r"|(?P<comment>/\*.*?\*/)"
    r"|(?P<quoted>'(?:''|\\.|[^'\\])*'|\"(?:\"\"|\\.|[^\"\\])*\"|\x60(?:\x60\x60|[^\x60])*\x60)"
    r"|(?P<word>[A-Za-z_][A-Za-z0-9_$]*)"
    r"|(?P<assign>:=)"
    r"|(?P<semicolon>;)"
    r"|(?P<other>.)",
    re.DOTALL,
)
_FORBIDDEN = {
    "INSERT", "UPDATE", "DELETE", "REPLACE", "MERGE",
    "CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME",
    "GRANT", "REVOKE", "CALL", "DO", "SET", "LOAD", "HANDLER",
    "LOCK", "UNLOCK", "OPTIMIZE", "REPAIR", "ANALYZE", "FLUSH", "KILL",
    "PREPARE", "EXECUTE", "DEALLOCATE", "COMMIT", "ROLLBACK",
    "SAVEPOINT", "START", "BEGIN", "TRANSACTION", "USE",
    "INTO", "FOR", "GET_LOCK", "RELEASE_LOCK", "SLEEP", "BENCHMARK", "LOAD_FILE",
}


def validate_readonly_sql(sql: str) -> str:
    """接受一个 SELECT/WITH 查询。采用保守规则，不充当完整 SQL 解析器。"""
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("SQL 不能为空。")

    tokens = []
    for match in _TOKEN.finditer(sql):
        kind, value = match.lastgroup, match.group()
        if kind in {"space", "line"}:
            continue
        if kind == "comment":
            if value.startswith(("/*!", "/*+", "/*M!")):
                raise ValueError("不接受可执行注释或优化器提示。")
            continue
        if kind == "quoted":
            # 消除 NO_BACKSLASH_ESCAPES 模式造成的引号解析歧义。
            if "\\" in value:
                raise ValueError("示例查询不支持含反斜杠的引号内容。")
        if kind == "other" and value in {"'", '"', "\x60"}:
            raise ValueError("SQL 中存在未闭合的引号。")
        if kind == "other" and value == "/" and sql[match.start():].startswith("/*"):
            raise ValueError("SQL 中存在未闭合的注释。")
        if kind == "assign":
            raise ValueError("查询不能包含变量赋值。")
        tokens.append((kind, value))

    if tokens and tokens[-1][0] == "semicolon":
        tokens.pop()
    if any(kind == "semicolon" for kind, _ in tokens):
        raise ValueError("每次只允许执行一条查询。")
    if not tokens or tokens[0][0] != "word" or tokens[0][1].upper() not in {"SELECT", "WITH"}:
        raise ValueError("只允许 SELECT 或以 WITH 开头的 SELECT 查询。")
    words = {value.upper() for kind, value in tokens if kind == "word"}
    if "SELECT" not in words or words.intersection(_FORBIDDEN):
        raise ValueError("查询包含不允许的操作、锁定子句或副作用函数。")
    return sql.strip().removesuffix(";").rstrip()


class DBManager:
    """延迟创建连接池；密码为必填参数，没有默认值。"""

    def __init__(
        self,
        username: str,
        password: str,
        database: str,
        host: str = "localhost",
        port: int = 3306,
        max_rows: int = 200,
    ):
        if not username or not password or not database:
            raise ValueError("数据库用户、密码和数据库名必须配置。")
        self.username = username
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.max_rows = max_rows
        self._engine = None

    @classmethod
    def from_env(cls):
        from ai_learning.config import mysql_settings
        return cls(**mysql_settings())

    def _connection_url(self) -> URL:
        return URL.create(
            "mysql+pymysql",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query={"charset": "utf8mb4"},
        )

    def _get_engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self._connection_url(),
                pool_size=5,
                max_overflow=5,
                pool_pre_ping=True,
                echo=False,
            )
        return self._engine

    def get_table_names(self) -> list[str]:
        return inspect(self._get_engine()).get_table_names()

    def get_table_names_with_comments(self) -> dict[str, str]:
        query = text(
            "SELECT table_name, table_comment FROM information_schema.tables "
            "WHERE table_schema = :database"
        )
        with self._get_engine().connect() as connection:
            rows = connection.execute(query, {"database": self.database})
            return {row[0]: row[1] or "" for row in rows}

    def get_all_table_schemas(self) -> dict[str, dict[str, Any]]:
        inspector = inspect(self._get_engine())
        comments = self.get_table_names_with_comments()
        result = {}
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "comment": column.get("comment") or "",
                })
            primary = inspector.get_pk_constraint(table_name) or {}
            result[table_name] = {
                "comment": comments.get(table_name, ""),
                "columns": columns,
                "primary_keys": primary.get("constrained_columns", []),
                "indexes": inspector.get_indexes(table_name),
            }
        return result

    def execute_query(self, sql: str) -> list[dict[str, Any]]:
        query = validate_readonly_sql(sql)
        with self._get_engine().connect() as connection:
            try:
                # 对下一事务设置 MySQL 只读模式；失败时不执行用户查询。
                connection.execute(text("SET TRANSACTION READ ONLY"))
                result = connection.execute(text(query))
                return [dict(row) for row in result.mappings().fetchmany(self.max_rows)]
            finally:
                connection.rollback()

    def close(self) -> None:
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
