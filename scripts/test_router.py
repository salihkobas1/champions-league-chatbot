import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.services.router_service import route_question


if __name__ == "__main__":
    questions = [
        "Who is the top scorer in Champions League history?",
        "Who is the 5th highest goalscorer?",
        "How many players scored more than 100 goals?",
        "What is the total number of goals by Portuguese players?",
        "List the top 5 clubs by titles.",
        "Tell me about Roy Makaay's fastest goal.",
        "Explain Cristiano Ronaldo's Champions League record.",
        "Give me details about Lionel Messi in the Champions League.",
        "List the top 3 goalscorers and explain their records.",
    ]

    for question in questions:
        route = route_question(question)
        print("=" * 70)
        print("Question:", question)
        print("Route:", route)