import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.core.config import RAG_CORPUS_PATH


def validate_rag_corpus():
    if not RAG_CORPUS_PATH.exists():
        print(f"RAG corpus not found: {RAG_CORPUS_PATH}")
        return

    print(f"RAG corpus found: {RAG_CORPUS_PATH}")

    with open(RAG_CORPUS_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    if not isinstance(docs, list):
        print("ERROR: RAG corpus must be a list.")
        return

    print(f"Total documents: {len(docs)}")

    missing_page_content = 0
    missing_metadata = 0
    empty_page_content = 0

    categories = {}

    for i, doc in enumerate(docs):
        if not isinstance(doc, dict):
            print(f"ERROR: Document at index {i} is not a dictionary.")
            continue

        if "page_content" not in doc:
            missing_page_content += 1
            print(f"Missing page_content at index {i}")

        if "metadata" not in doc:
            missing_metadata += 1
            print(f"Missing metadata at index {i}")

        page_content = doc.get("page_content", "")

        if not isinstance(page_content, str) or not page_content.strip():
            empty_page_content += 1
            print(f"Empty page_content at index {i}")

        metadata = doc.get("metadata", {})
        category = metadata.get("category", "unknown")
        categories[category] = categories.get(category, 0) + 1

    print("\nValidation summary:")
    print(f"Missing page_content: {missing_page_content}")
    print(f"Missing metadata: {missing_metadata}")
    print(f"Empty page_content: {empty_page_content}")

    print("\nCategory distribution:")
    for category, count in categories.items():
        print(f"  {category}: {count}")

    if missing_page_content == 0 and missing_metadata == 0 and empty_page_content == 0:
        print("\nRAG corpus looks valid.")


if __name__ == "__main__":
    validate_rag_corpus()