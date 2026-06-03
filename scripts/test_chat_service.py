import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.services.chat_service import answer_question


def print_response(question, response):
    print("\n" + "=" * 80)
    print("Question:", question)
    print("=" * 80)

    print("Route:", response["route"])
    print("Answer:", response["answer"])

    if response.get("sql_intent"):
        print("SQL Intent:", response["sql_intent"])

    if response.get("sql_result") is not None:
        print("SQL Result:")
        for row in response["sql_result"]:
            print(row)

    if response.get("retrieved_docs"):
        print("Retrieved Docs:")
        for i, doc in enumerate(response["retrieved_docs"], start=1):
            print(f"\nDoc {i}")
            print("Score:", doc["score"])
            print("Content:", doc["page_content"])
            print("Metadata:", doc["metadata"])


if __name__ == "__main__":
    questions = [
        "Who is the top 5 scorer in Champions League history?",
        "Who is the 5th highest goalscorer?",
        "How many players scored more than 100 goals?",
        "What is the total number of goals by Portuguese players?",
        "Tell me about Roy Makaay's fastest goal.",
        "List the top 3 goalscorers and explain their records.",
    ]

    for question in questions:
        response = answer_question(question)
        print_response(question, response)