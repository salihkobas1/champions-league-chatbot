import time
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.services.chat_service import answer_question


EVAL_DATASET = [
    {
        "question": "Who is the 5th highest goalscorer?",
        "expected_route": "sql",
        "expected_answer": "Raúl González",
    },
    {
        "question": "How many players scored more than 100 goals?",
        "expected_route": "sql",
        "expected_answer": "2",
    },
    {
        "question": "How many goals did Messi score?",
        "expected_route": "sql",
        "expected_answer": "129",
    },
    {
        "question": "How many titles does Real Madrid have?",
        "expected_route": "sql",
        "expected_answer": "14",
    },
    {
        "question": "Is Cristiano Ronaldo the top scorer of UCL history?",
        "expected_route": "hybrid",
        "expected_answer": "Cristiano Ronaldo",
        "expected_metadata": {
            "player": "Cristiano Ronaldo",
            "category": "all_time_goalscorers",
        },
    },
    {
        "question": "Who is the top scorer of UCL history?",
        "expected_route": "sql",
        "expected_answer": "Cristiano Ronaldo",
    },
    {
        "question": "Tell me about Neymar.",
        "expected_route": "rag",
        "expected_answer": "Neymar",
        "expected_metadata": {
            "player": "Neymar",
            "category": "all_time_goalscorers",
        },
    },
    {
        "question": "Tell me about Alessandro Del Piero.",
        "expected_route": "rag",
        "expected_answer": "Alessandro Del Piero",
        "expected_metadata": {
            "player": "Alessandro Del Piero",
            "category": "all_time_goalscorers",
        },
    },
    {
        "question": "List the top 3 goalscorers and explain their records.",
        "expected_route": "hybrid",
        "expected_answer": "Cristiano Ronaldo",
        "expected_metadata": {
            "player": "Cristiano Ronaldo",
            "category": "all_time_goalscorers",
        },
    },
]


def check_answer(expected_answer, generated_answer):
    return expected_answer.lower() in generated_answer.lower()


def evaluate_retrieval(expected_metadata, retrieved_docs):
    if not expected_metadata or not retrieved_docs:
        return None, None

    expected_player = expected_metadata.get("player")
    expected_category = expected_metadata.get("category")

    for rank, doc in enumerate(retrieved_docs, start=1):
        metadata = doc.get("metadata", {})

        player_match = (
            expected_player is None
            or metadata.get("player", "").lower() == expected_player.lower()
        )

        category_match = (
            expected_category is None
            or metadata.get("category", "").lower() == expected_category.lower()
        )

        if player_match and category_match:
            recall_at_k = 1
            mrr = 1 / rank
            return recall_at_k, mrr

    return 0, 0


def run_evaluation():
    total = len(EVAL_DATASET)

    route_correct = 0
    answer_correct = 0

    retrieval_count = 0
    recall_sum = 0
    mrr_sum = 0

    latencies = []

    print("Running evaluation...\n")

    for item in EVAL_DATASET:
        question = item["question"]

        start_time = time.time()
        response = answer_question(question)
        end_time = time.time()

        latency = end_time - start_time
        latencies.append(latency)

        predicted_route = response.get("route")
        answer = response.get("answer", "")
        retrieved_docs = response.get("retrieved_docs")

        expected_route = item["expected_route"]
        expected_answer = item["expected_answer"]

        is_route_correct = predicted_route == expected_route
        is_answer_correct = check_answer(expected_answer, answer)

        if is_route_correct:
            route_correct += 1

        if is_answer_correct:
            answer_correct += 1

        recall_at_k = None
        mrr = None

        if "expected_metadata" in item:
            retrieval_count += 1
            recall_at_k, mrr = evaluate_retrieval(
                item["expected_metadata"],
                retrieved_docs,
            )
            recall_sum += recall_at_k
            mrr_sum += mrr

        print("=" * 80)
        print("Question:", question)
        print("Expected route:", expected_route)
        print("Predicted route:", predicted_route)
        print("Route correct:", is_route_correct)
        print("Expected answer:", expected_answer)
        print("Generated answer:", answer)
        print("Answer correct:", is_answer_correct)
        print("Latency:", round(latency, 3), "seconds")

        if recall_at_k is not None:
            print("Recall@k:", recall_at_k)
            print("MRR:", round(mrr, 3))

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print("Route Accuracy:", round(route_correct / total, 3))
    print("Answer Accuracy:", round(answer_correct / total, 3))
    print("Average Latency:", round(sum(latencies) / len(latencies), 3), "seconds")
    print("Max Latency:", round(max(latencies), 3), "seconds")

    if retrieval_count > 0:
        print("Retrieval Recall@k:", round(recall_sum / retrieval_count, 3))
        print("Retrieval MRR:", round(mrr_sum / retrieval_count, 3))


if __name__ == "__main__":
    run_evaluation()