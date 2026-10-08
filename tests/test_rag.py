"""RAG 离线回归测试：不安装 LangChain、不提供密钥也不会联网。"""
import importlib.util
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, patch
from lessons.rag_basics.helpers import cosine_similarity
from lessons.hybrid_search.helpers import reciprocal_rank_fusion, sample_documents
from projects.smart_reading.config.setting import QaConfig

ROOT = Path(__file__).resolve().parents[1]


def load_source(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_module(name, **members):
    module = ModuleType(name)
    module.__dict__.update(members)
    return module


class RetrievalTests(unittest.TestCase):
    def test_cosine_direction_and_zero_vector(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [4, 0]), 1.0)
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 4]), 0.0)
        with self.assertRaises(ValueError):
            cosine_similarity([0, 0], [1, 0])

    def test_rrf_prefers_document_supported_by_both_rankings(self):
        results = reciprocal_rank_fusion([[(0, 100), (1, 3)], [(1, 500), (2, 4)]])
        self.assertEqual(results[0][0], 1)
        self.assertAlmostEqual(results[0][1], 1/62 + 1/61)
        self.assertEqual(reciprocal_rank_fusion([]), [])

    def test_examples_are_original_fictional_data(self):
        documents = sample_documents()
        self.assertTrue(any("Aurora-4" in document for document in documents))
        self.assertTrue(all("GPT" not in document for document in documents))
        self.assertTrue((ROOT / "assets" / "learning_guide.pdf").is_file())

    def test_configuration_has_no_directory_creation_side_effect(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "not-created"
            QaConfig(chroma_root_dir=target)
            self.assertFalse(target.exists())
        with self.assertRaises(ValueError):
            QaConfig(chunk_size=20, chunk_overlap=20)

    def test_original_question_reaches_answer_generator(self):
        rewriter = Mock()
        rewriter.return_value.rewrite.return_value = "社团项目的第二阶段要完成什么？"
        reranker = Mock()
        reranker.return_value.rerank.return_value = ([object()], "evidence")
        generator = Mock()
        generator.return_value.generate.return_value = "完成文档检索。[1]"
        stubs = {
            "langchain_community": fake_module("langchain_community"),
            "langchain_community.chat_models": fake_module("chat_models", ChatTongyi=Mock()),
            "langchain_community.embeddings": fake_module("embeddings", DashScopeEmbeddings=Mock()),
            "projects.smart_reading.indexing.vectorstorage": fake_module("vectorstorage", VectorStoreManager=Mock()),
            "projects.smart_reading.querying.query_rewrite": fake_module("query_rewrite", QueryRewriter=rewriter),
            "projects.smart_reading.querying.rerank": fake_module("rerank", RerankPipeline=reranker),
            "projects.smart_reading.querying.answer": fake_module("answer", AnswerGenerator=generator),
            "projects.smart_reading.querying.vector_retriever": fake_module("vector_retriever", recall_with_scores=Mock(return_value=([object()], [0.8]))),
        }
        with patch.dict(sys.modules, stubs):
            module = load_source("projects.smart_reading.querying.offline_pipeline", "projects/smart_reading/querying/query_pipeline.py")
            pipeline = module.RagPipeline(QaConfig())
            pipeline._init_llm = Mock(return_value=object())
            pipeline._load_vectorstore = Mock(return_value=object())
            result = pipeline.query("offline-test", "hash", "它的第二阶段要完成什么？", [])
        self.assertNotIn("error", result)
        self.assertTrue(result["rewritten"])
        generator.return_value.generate.assert_called_once_with("它的第二阶段要完成什么？", [], "evidence")

    def test_service_error_does_not_enter_chat_history(self):
        class History:
            def __init__(self): self.messages = []
            def add_user_message(self, content): self.messages.append(("user", content))
            def add_ai_message(self, content): self.messages.append(("assistant", content))
        stubs = {
            "langchain_core": fake_module("langchain_core"),
            "langchain_core.chat_history": fake_module("chat_history", InMemoryChatMessageHistory=History),
            "projects.smart_reading.indexing.indexing_pipeline": fake_module("indexing_pipeline", IndexingPipeline=Mock()),
            "projects.smart_reading.querying.query_pipeline": fake_module("query_pipeline", RagPipeline=Mock()),
        }
        with patch.dict(sys.modules, stubs):
            module = load_source("projects.smart_reading.offline_run", "projects/smart_reading/run.py")
            qa = module.PDFQA("sample.pdf", api_key="offline-test")
            qa.file_hash = "hash"
            qa.rag = Mock()
            qa.rag.query.return_value = {"error": "unavailable", "answer": "temporary failure"}
            qa.ask("项目多久？")
            self.assertEqual(qa.chat_history.messages, [])
            qa.rag.query.return_value = {"answer": "六周"}
            qa.ask("项目多久？")
            self.assertEqual(len(qa.chat_history.messages), 2)


if __name__ == "__main__":
    unittest.main()
