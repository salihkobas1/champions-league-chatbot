from app.services.router_service import route_question
from app.services.rag_service import RagService
from app.services.sql_service import (
    get_top_goalscorers,
    get_nth_top_goalscorer,
    count_players_with_more_than_goals,
    get_total_goals_by_nationality,
    get_players_by_nationality,
    get_top_clubs_by_titles,
    get_nth_club_by_ranking,
    get_top_players_by_appearances,
    get_season_top_scorer,
    get_most_goals_single_game,
    get_player_goals,
    get_player_appearances,
    get_club_titles,
    get_club_by_most_titles,
    get_player_with_most_goals,
    get_player_with_most_appearances,
)
from app.services.answer_formatter_service import (
    format_sql_answer,
    format_rag_answer,
    format_hybrid_answer,
)

from app.services.source_formatter_service import (
    format_sql_sources,
    format_rag_sources,
    format_hybrid_sources,
)

rag_service = None


def get_rag_service():
    """
    Loads RagService only once.
    This prevents reloading the embedding model for every user question.
    """
    global rag_service

    if rag_service is None:
        rag_service = RagService()

    return rag_service


def detect_simple_sql_intent(question: str):
    """
    Temporary rule-based SQL intent detector.
    Later, we can replace or improve this with Text-to-SQL.
    """

    q = question.lower()

    if "who" in q and "most" in q and "goal" in q and ("player" in q or "scored" in q or "has" in q):
        return {
            "intent": "player_with_most_goals",
            "result": get_player_with_most_goals(),
        }

    # Player with most appearances
    if "who" in q and "most" in q and ("appearance" in q or "appearances" in q or "matches" in q):
        return {
            "intent": "player_with_most_appearances",
            "result": get_player_with_most_appearances(),
        }

    # Club with most titles
    if "club" in q and "most" in q and "title" in q:
        return {
            "intent": "club_with_most_titles",
            "result": get_club_by_most_titles(),
        }

    # Specific player goals
    player_name = detect_player_name(q)

    if player_name and "goal" in q:
        return {
            "intent": "player_goals",
            "result": get_player_goals(player_name),
        }

    # Specific player appearances
    if player_name and ("appearance" in q or "appearances" in q or "matches" in q):
        return {
            "intent": "player_appearances",
            "result": get_player_appearances(player_name),
        }

    # Specific club titles
    club_name = detect_club_name(q)

    if club_name and "title" in q:
        return {
            "intent": "club_titles",
            "result": get_club_titles(club_name),
        }







    # Top goalscorers
    if "top" in q and "scorer" in q:
        limit = extract_number(q, default=5)
        return {
            "intent": "top_goalscorers",
            "result": get_top_goalscorers(limit),
        }

    # Nth highest goalscorer
    if ("5th" in q or "fifth" in q) and ("scorer" in q or "goalscorer" in q):
        return {
            "intent": "nth_top_goalscorer",
            "result": get_nth_top_goalscorer(5),
        }

    # Count players above goal threshold
    if "how many" in q and "more than" in q and "goal" in q:
        threshold = extract_number(q, default=100)
        return {
            "intent": "count_players_with_more_than_goals",
            "result": count_players_with_more_than_goals(threshold),
        }

    # Total goals by nationality
    if "total" in q and "goal" in q:
        nationality = detect_nationality(q)

        if nationality:
            return {
                "intent": "total_goals_by_nationality",
                "result": get_total_goals_by_nationality(nationality),
            }

    # Players by nationality
    if "players" in q and ("from" in q or "nationality" in q):
        nationality = detect_nationality(q)

        if nationality:
            return {
                "intent": "players_by_nationality",
                "result": get_players_by_nationality(nationality),
            }

    # Top clubs by titles
    if "top" in q and "club" in q:
        limit = extract_number(q, default=5)
        return {
            "intent": "top_clubs_by_titles",
            "result": get_top_clubs_by_titles(limit),
        }

    if "club" in q and ("ranked" in q or "ranking" in q):
        rank = extract_number(q, default=1)
        return {
            "intent": "nth_club_by_ranking",
            "result": get_nth_club_by_ranking(rank),
        }

    # Top players by appearances
    if "appearance" in q or "appearances" in q or "matches" in q:
        limit = extract_number(q, default=5)
        return {
            "intent": "top_players_by_appearances",
            "result": get_top_players_by_appearances(limit),
        }

    # Season top scorer
    season = detect_season(q)
    if season and "scorer" in q:
        return {
            "intent": "season_top_scorer",
            "result": get_season_top_scorer(season),
        }

    # Most goals in single game
    if "single game" in q or "one game" in q:
        limit = extract_number(q, default=5)
        return {
            "intent": "most_goals_single_game",
            "result": get_most_goals_single_game(limit),
        }

    return {
        "intent": "unknown_sql_intent",
        "result": [],
    }


def extract_number(text: str, default: int = 5):
    """
    Extracts the first integer from a question.
    Example:
    'top 3 scorers' -> 3
    'more than 100 goals' -> 100
    """

    words = text.replace("?", "").replace(".", "").split()

    for word in words:
        if word.isdigit():
            return int(word)

        if word.endswith("st") or word.endswith("nd") or word.endswith("rd") or word.endswith("th"):
            number_part = word[:-2]
            if number_part.isdigit():
                return int(number_part)

    return default


def detect_nationality(text: str):
    """
    Temporary nationality detector.
    We can expand this list depending on the dataset.
    """

    nationality_map = {
        "portuguese": "Portugal",
        "portugal": "Portugal",
        "argentinian": "Argentina",
        "argentine": "Argentina",
        "argentina": "Argentina",
        "brazilian": "Brazil",
        "brazil": "Brazil",
        "spanish": "Spain",
        "spain": "Spain",
        "french": "France",
        "france": "France",
        "polish": "Poland",
        "poland": "Poland",
        "german": "Germany",
        "germany": "Germany",
        "english": "England",
        "england": "England",
        "italian": "Italy",
        "italy": "Italy",
    }

    for key, value in nationality_map.items():
        if key in text:
            return value

    return None


def detect_player_name(text: str):
    """
    Temporary player detector for popular players in the dataset.
    This can later be replaced with a dynamic database lookup.
    """

    player_map = {
        "ronaldo": "Cristiano Ronaldo",
        "cristiano": "Cristiano Ronaldo",
        "cristiano ronaldo": "Cristiano Ronaldo",
        "messi": "Lionel Messi",
        "lionel messi": "Lionel Messi",
        "lewandowski": "Robert Lewandowski",
        "robert lewandowski": "Robert Lewandowski",
        "benzema": "Karim Benzema",
        "karim benzema": "Karim Benzema",
        "raul": "Raúl González",
        "raúl": "Raúl González",
        "raul gonzalez": "Raúl González",
        "raúl gonzález": "Raúl González",
        "neymar": "Neymar",
        "mbappe": "Kylian Mbappé",
        "mbappé": "Kylian Mbappé",
        "van nistelrooy": "Ruud van Nistelrooy",
        "shevchenko": "Andriy Shevchenko",
        "henry": "Thierry Henry",
        "zlatan": "Zlatan Ibrahimović",
        "ibrahimovic": "Zlatan Ibrahimović",
    }

    for key, value in player_map.items():
        if key in text:
            return value

    return None


def detect_club_name(text: str):
    """
    Temporary club detector for common Champions League clubs.
    """

    club_map = {
        "real madrid": "Real Madrid CF",
        "madrid": "Real Madrid CF",
        "bayern": "FC Bayern München",
        "bayern munich": "FC Bayern München",
        "barcelona": "FC Barcelona",
        "barca": "FC Barcelona",
        "manchester united": "Manchester United FC",
        "man united": "Manchester United FC",
        "milan": "AC Milan",
        "ac milan": "AC Milan",
        "liverpool": "Liverpool FC",
        "juventus": "Juventus",
        "chelsea": "Chelsea FC",
        "psg": "Paris Saint-Germain",
        "paris saint-germain": "Paris Saint-Germain",
        "inter": "FC Internazionale Milano",
        "ajax": "AFC Ajax",
    }

    for key, value in club_map.items():
        if key in text:
            return value

    return None



def detect_season(text: str):
    """
    Detects season formats like 2014/15.
    """

    words = text.replace("?", "").replace(".", "").split()

    for word in words:
        if "/" in word:
            left, right = word.split("/", 1)

            if left.isdigit() and right.isdigit():
                return word

    return None


def answer_question(question: str):
    route = route_question(question)

    if route == "sql":
        sql_payload = detect_simple_sql_intent(question)

        final_answer = format_sql_answer(
            question,
            sql_payload["intent"],
            sql_payload["result"],
        )

        return {
            "route": "sql",
            "answer": final_answer,
            "sql_intent": sql_payload["intent"],
            "sql_result": sql_payload["result"],
            "retrieved_docs": None,
            "sources": None,
        }

    if route == "rag":
        rag = get_rag_service()
        retrieved_docs = rag.retrieve(question, top_k=5)

        final_answer = format_rag_answer(retrieved_docs)

        return {
            "route": "rag",
            "answer": final_answer,
            "sql_intent": None,
            "sql_result": None,
            "retrieved_docs": retrieved_docs,
            "sources": None,
        }

    if route == "hybrid":
        sql_payload = detect_simple_sql_intent(question)

        rag = get_rag_service()
        retrieved_docs = rag.retrieve(question, top_k=5)

        final_answer = format_hybrid_answer(
            sql_payload["intent"],
            sql_payload["result"],
            retrieved_docs,
        )

        return {
            "route": "hybrid",
            "answer": final_answer,
            "sql_intent": sql_payload["intent"],
            "sql_result": sql_payload["result"],
            "retrieved_docs": retrieved_docs,
            "sources": None,
        }

    return {
        "route": "unknown",
        "answer": "Could not route the question.",
        "sql_intent": None,
        "sql_result": None,
        "retrieved_docs": None,
        "sources": None,
    }