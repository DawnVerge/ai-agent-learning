"""不连接数据库的只读 SQL、事务与配置测试。"""

import importlib
import unittest
from unittest.mock import MagicMock, patch


MODULES = (
    "projects.text_to_sql.db_manager",
    "projects.database_mcp.db_manager",
)


class DatabaseTests(unittest.TestCase):
    def test_allowed_single_queries(self):
        queries = (
            "SELECT 1",
            "SELECT 'a;b' AS example;",
            "/* ordinary comment */ SELECT name FROM products LIMIT 5",
            "WITH totals AS (SELECT product_id FROM orders) SELECT * FROM totals",
            "SELECT 'DROP TABLE products' AS harmless_text",
            "SELECT 1; -- trailing comment",
        )
        for name in MODULES:
            module = importlib.import_module(name)
            for query in queries:
                with self.subTest(module=name, sql=query):
                    self.assertIsInstance(module.validate_readonly_sql(query), str)

    def test_rejects_write_multiple_and_ambiguous_queries(self):
        queries = (
            "",
            "DELETE FROM orders",
            "SELECT 1; DROP TABLE products",
            "SELECT 1; SELECT 2",
            "WITH x AS (SELECT 1) DELETE FROM orders",
            "SELECT * INTO OUTFILE '/tmp/example' FROM products",
            "SELECT * FROM products FOR UPDATE",
            "SELECT * FROM products LOCK IN SHARE MODE",
            "SELECT /*!50000 SLEEP(10) */ 1",
            "SELECT /*+ SET_VAR(example=1) */ 1",
            "SELECT GET_LOCK('demo', 1)",
            "SELECT @value := 1",
            "SELECT 'unterminated",
            "SELECT 1 /* unterminated",
            r"SELECT 'back\slash'",
        )
        for name in MODULES:
            module = importlib.import_module(name)
            for query in queries:
                with self.subTest(module=name, sql=query):
                    with self.assertRaises(ValueError):
                        module.validate_readonly_sql(query)

    def test_rejected_query_does_not_create_engine(self):
        for name in MODULES:
            module = importlib.import_module(name)
            manager = module.DBManager("demo", "unit-test-value", "demo")
            with patch.object(module, "create_engine") as create_engine:
                with self.assertRaises(ValueError):
                    manager.execute_query("DROP TABLE products")
                create_engine.assert_not_called()

    def test_special_characters_in_password_use_url_object(self):
        for name in MODULES:
            module = importlib.import_module(name)
            manager = module.DBManager("demo", "test@:/# value", "demo")
            with patch.object(module, "create_engine") as create_engine:
                manager._get_engine()
                url = create_engine.call_args.args[0]
                self.assertEqual(url.password, "test@:/# value")
                self.assertEqual(url.database, "demo")
                self.assertNotIn("test@:/# value", str(url))

    def test_query_sets_readonly_and_always_rolls_back(self):
        for name in MODULES:
            module = importlib.import_module(name)
            manager = module.DBManager("demo", "unit-test-value", "demo", max_rows=7)
            engine = MagicMock()
            connection = engine.connect.return_value.__enter__.return_value
            result = MagicMock()
            result.mappings.return_value.fetchmany.return_value = [{"name": "example"}]
            connection.execute.side_effect = [None, result]
            manager._engine = engine

            self.assertEqual(manager.execute_query("SELECT name FROM products"), [{"name": "example"}])
            statements = [str(call.args[0]) for call in connection.execute.call_args_list]
            self.assertEqual(statements, ["SET TRANSACTION READ ONLY", "SELECT name FROM products"])
            result.mappings.return_value.fetchmany.assert_called_once_with(7)
            connection.rollback.assert_called_once()

    def test_readonly_failure_prevents_user_query(self):
        for name in MODULES:
            module = importlib.import_module(name)
            manager = module.DBManager("demo", "unit-test-value", "demo")
            engine = MagicMock()
            connection = engine.connect.return_value.__enter__.return_value
            connection.execute.side_effect = RuntimeError("read-only setup failed")
            manager._engine = engine
            with self.assertRaises(RuntimeError):
                manager.execute_query("SELECT 1")
            self.assertEqual(connection.execute.call_count, 1)
            connection.rollback.assert_called_once()

    def test_query_failure_still_rolls_back(self):
        for name in MODULES:
            module = importlib.import_module(name)
            manager = module.DBManager("demo", "unit-test-value", "demo")
            engine = MagicMock()
            connection = engine.connect.return_value.__enter__.return_value
            connection.execute.side_effect = [None, RuntimeError("query failed")]
            manager._engine = engine
            with self.assertRaises(RuntimeError):
                manager.execute_query("SELECT 1")
            connection.rollback.assert_called_once()

    def test_credentials_are_required_without_defaults(self):
        for name in MODULES:
            module = importlib.import_module(name)
            with self.assertRaises(TypeError):
                module.DBManager(username="demo", database="demo")
            with self.assertRaises(ValueError):
                module.DBManager(username="demo", password="", database="demo")


if __name__ == "__main__":
    unittest.main()
