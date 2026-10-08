"""查询改写、向量召回、LLM 重排与有依据回答。"""
from typing import Any, Dict
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from ..config.setting import QaConfig
from ..indexing.vectorstorage import VectorStoreManager
from .query_rewrite import QueryRewriter
from .rerank import RerankPipeline
from .answer import AnswerGenerator
from .vector_retriever import recall_with_scores

class RagPipeline:
    def __init__(self, config: QaConfig):
        self.cfg = config
        self._llm = None
        self._embeddings = None
        self._vectorstores = {}

    def _init_llm(self, api_key):
        if self._llm is None:
            self._llm = ChatTongyi(model=self.cfg.chat_model, dashscope_api_key=api_key)
        return self._llm

    def _init_embeddings(self, api_key):
        if self._embeddings is None:
            self._embeddings = DashScopeEmbeddings(model=self.cfg.embedding_model, dashscope_api_key=api_key)
        return self._embeddings

    def _load_vectorstore(self, file_hash, api_key):
        if file_hash not in self._vectorstores:
            manager = VectorStoreManager(self.cfg, self._init_embeddings(api_key))
            self._vectorstores[file_hash] = manager.load_or_build(file_hash)
        return self._vectorstores[file_hash]

    def query(self, dashscope_api_key, file_hash, question, chat_history, *, top_k=4, recall_k=10) -> Dict[str, Any]:
        search_query = question
        try:
            if not question.strip() or top_k <= 0 or recall_k <= 0:
                raise ValueError("问题不能为空，召回数量和最终数量必须大于零")
            llm = self._init_llm(dashscope_api_key)
            vectorstore = self._load_vectorstore(file_hash, dashscope_api_key)
            search_query = QueryRewriter(llm).rewrite(question, chat_history)
            documents, scores = recall_with_scores(search_query, vectorstore, k=recall_k)
            evidence, context = RerankPipeline(self.cfg, llm).rerank(
                query=search_query, recalled_docs=documents, vec_scores=scores, final_top_n=top_k,
            )
            # 改写问题只用于检索；最终回答保留用户的原始表达。
            answer = AnswerGenerator(llm).generate(question, chat_history, context) if evidence else "当前文档未找到足够依据来回答这个问题。"
            return {"answer": answer, "context": context, "evidence": evidence,
                    "search_query": search_query, "rewritten": search_query != question, "doc_count": len(evidence)}
        except Exception as exc:
            return {"error": f"查询失败：{exc}", "answer": "处理请求时出现错误，请检查配置后重试。",
                    "context": "", "evidence": [], "search_query": search_query,
                    "rewritten": search_query != question, "doc_count": 0}
