import json
import pickle
import sys
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.core.config import (
    RAG_CORPUS_PATH,
    RAG_INDEX_DIR,
    FAISS_INDEX_PATH,
    DOCUMENTS_PATH,
    METADATA_PATH,
)


EMBEDDING_MODEL_NAME = "BAAI/bge-m3"


def load_rag_corpus():
    if not RAG_CORPUS_PATH.exists():
        raise FileNotFoundError(f"RAG corpus not found: {RAG_CORPUS_PATH}")

    with open(RAG_CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    if not isinstance(corpus, list):
        raise ValueError("RAG corpus must be a list of documents.")

    return corpus


def build_faiss_index():
    print("Loading RAG corpus...")
    corpus = load_rag_corpus()

    documents = []
    metadata = []

    for i, doc in enumerate(corpus):
        page_content = doc.get("page_content", "").strip()

        if not page_content:
            print(f"Skipping empty document at index {i}")
            continue

        documents.append(page_content)
        metadata.append(doc.get("metadata", {}))

    print(f"Total valid documents: {len(documents)}")

    if not documents:
        raise ValueError("No valid documents found in RAG corpus.")

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Creating embeddings...")
    embeddings = model.encode(
        documents,
        batch_size=16,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = embeddings.astype("float32")

    print(f"Embeddings shape: {embeddings.shape}")

    dimension = embeddings.shape[1]

    # Since embeddings are normalized, IndexFlatIP behaves like cosine similarity.
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    print(f"FAISS index created with {index.ntotal} vectors.")

    RAG_INDEX_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    with open(DOCUMENTS_PATH, "wb") as f:
        pickle.dump(documents, f)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("\nFAISS files saved successfully:")
    print(f"Index: {FAISS_INDEX_PATH}")
    print(f"Documents: {DOCUMENTS_PATH}")
    print(f"Metadata: {METADATA_PATH}")


if __name__ == "__main__":
    build_faiss_index()