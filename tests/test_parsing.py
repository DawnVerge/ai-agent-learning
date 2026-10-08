import unittest
from ai_learning.parsing import extract_json_object


class JsonExtractionTests(unittest.TestCase):
    def test_fenced_nested_object(self):
        text = '说明\n```json\n{"intents":["refund"],"slots":{"order":"ORD1"}}\n```'
        self.assertEqual(extract_json_object(text)["slots"]["order"], "ORD1")

    def test_missing_or_invalid_output_returns_empty_mapping(self):
        for text in (None, "", "   ", "not json", "[]", "{broken}"):
            with self.subTest(text=text):
                self.assertEqual(extract_json_object(text), {})


if __name__ == "__main__":
    unittest.main()
