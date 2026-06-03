import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.services.chat_service import answer_question


def print_bot_response(response):
    print("\nBot:")
    print(response["answer"])

    print("\nDebug Info:")
    print(f"Route: {response.get('route')}")
    print(f"SQL Intent: {response.get('sql_intent')}")

    if response.get("sql_result"):
        print("SQL Result:")
        for row in response["sql_result"]:
            print(row)

    if response.get("retrieved_docs"):
        print("Retrieved Docs:")
        for i, doc in enumerate(response["retrieved_docs"][:3], start=1):
            print(f"\nDoc {i}")
            print("Score:", doc.get("score"))
            print("Content:", doc.get("page_content"))
            print("Metadata:", doc.get("metadata"))


def main():
    print("Champions League Chatbot CLI")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break

        if not question:
            continue

        try:
            response = answer_question(question)
            print_bot_response(response)
            print("\n" + "-" * 80 + "\n")

        except Exception as e:
            print("\nBot: An error occurred.")
            print("Error:", e)
            print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()