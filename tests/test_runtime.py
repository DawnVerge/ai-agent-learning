import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_learning.cli import main
from ai_learning.config import PROJECT_ROOT, get_api_key, load_environment, mysql_settings
from ai_learning.validation import check_repository


class EnvironmentTests(unittest.TestCase):
    def test_env_load_preserves_shell_values_and_aliases_key(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            path = Path(directory) / ".env"
            path.write_text("DASHSCOPE_MODEL=file-model\nDASHSCOPE_API_KEY='test-value'\nEMPTY=\n", encoding="utf-8")
            os.environ["DASHSCOPE_MODEL"] = "shell-model"
            load_environment(path)
            self.assertEqual(os.environ["DASHSCOPE_MODEL"], "shell-model")
            self.assertEqual(os.environ["OPENAI_API_KEY"], "test-value")
            self.assertEqual(os.environ["EMPTY"], "")

    def test_missing_key_reports_variable_without_secret(self):
        with patch.dict(os.environ, {}, clear=True), patch("ai_learning.config.load_environment"):
            with self.assertRaisesRegex(ValueError, "DASHSCOPE_API_KEY"):
                get_api_key()

    def test_database_configuration_has_no_password_default(self):
        with patch.dict(os.environ, {}, clear=True), patch("ai_learning.config.load_environment"):
            with self.assertRaisesRegex(ValueError, "MYSQL_PASSWORD"):
                mysql_settings()

    def test_env_invalid_quote_does_not_include_value_in_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text('VALUE="private-value\n', encoding="utf-8")
            with self.assertRaises(ValueError) as error:
                load_environment(path)
            self.assertNotIn("private-value", str(error.exception))


class RepositoryTests(unittest.TestCase):
    def test_repository_is_valid(self):
        self.assertEqual(check_repository(), [])

    def test_offline_catalog_does_not_import_integrations(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(main(["list", "--offline"]), 0)
        self.assertIn("prompts.10", stream.getvalue())
        self.assertNotIn("project.pdf-qa", stream.getvalue())

    def test_catalog_contains_all_four_projects(self):
        catalog = json.loads((PROJECT_ROOT / "ai_learning/catalog.json").read_text(encoding="utf-8"))
        ids = {item["id"] for item in catalog}
        self.assertTrue({"project.chat", "project.pdf-qa", "project.text-to-sql", "project.database-mcp"} <= ids)

    def test_lesson_help_never_starts_the_example(self):
        with patch("ai_learning.cli.subprocess.run") as run, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["run", "model-api.01", "--", "--help"]), 0)
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
