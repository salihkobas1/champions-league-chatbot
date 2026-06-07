from sentence_transformers import CrossEncoder

from app.core.config import RERANKER_MODEL_NAME


class RerankerService:
    def __init__(self):
        print(f"Loading reranker model: {RERANKER_MODEL_NAME}")
        self.model = CrossEncoder(RERANKER_MODEL_NAME)

    def rerank(self, query: str, documents: list, top_k: int = 5):
        if not documents:
            return []

        pairs = [
            [query, doc["page_content"]]
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        reranked_docs = []

        for doc, score in zip(documents, scores):
            new_doc = doc.copy()
            new_doc["rerank_score"] = float(score)
            reranked_docs.append(new_doc)

        reranked_docs.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked_docs[:top_k]


reranker_service = None


def get_reranker_service():
    global reranker_service

    if reranker_service is None:
        reranker_service = RerankerService()

    return reranker_service