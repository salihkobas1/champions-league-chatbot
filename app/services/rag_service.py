import pickle

import faiss
from sentence_transformers import SentenceTransformer

from app.core.config import (
    FAISS_INDEX_PATH,
    DOCUMENTS_PATH,
    METADATA_PATH,
)


EMBEDDING_MODEL_NAME = "BAAI/bge-m3"


class RagService:
    def __init__(self):
        if not FAISS_INDEX_PATH.exists():
            raise FileNotFoundError(f"FAISS index not found: {FAISS_INDEX_PATH}")

        if not DOCUMENTS_PATH.exists():
            raise FileNotFoundError(f"Documents file not found: {DOCUMENTS_PATH}")

        if not METADATA_PATH.exists():
            raise FileNotFoundError(f"Metadata file not found: {METADATA_PATH}")

        print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        print(f"Loading FAISS index from: {FAISS_INDEX_PATH}")
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        with open(DOCUMENTS_PATH, "rb") as f:
            self.documents = pickle.load(f)

        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        print(f"Loaded {len(self.documents)} documents.")
        print(f"FAISS index contains {self.index.ntotal} vectors.")

    def retrieve(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype("float32")

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            results.append(
                {
                    "score": float(score),
                    "page_content": self.documents[idx],
                    "metadata": self.metadata[idx],
                }
            )

        return results