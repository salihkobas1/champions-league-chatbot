import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.services.rag_service import RagService


def print_results(query, results):
    print("\n" + "=" * 80)
    print("Query:", query)
    print("=" * 80)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("-" * 40)
        print("Score:", result["score"])
        print("Content:", result["page_content"])
        print("Metadata:", result["metadata"])


if __name__ == "__main__":
    rag = RagService()

    test_queries = [
        "Tell me about Roy Makaay's fastest goal.",
        "Who scored one of the fastest goals in Champions League history?",
        "Cristiano Ronaldo Champions League goals",
        "Lionel Messi all time Champions League goals",
        "IS there any Bosnian top goalscorer in Champions League history?",
    ]

    for query in test_queries:
        results = rag.retrieve(query, top_k=5)
        print_results(query, results)