def format_sql_sources(sql_intent: str):
    intent_to_table = {
        "top_goalscorers": "top_goalscorers",
        "nth_top_goalscorer": "top_goalscorers",
        "count_players_with_more_than_goals": "top_goalscorers",
        "total_goals_by_nationality": "top_goalscorers",
        "players_by_nationality": "top_goalscorers",
        "top_clubs_by_titles": "club_ranking",
        "nth_club_by_ranking": "club_ranking",
        "top_players_by_appearances": "player_appearances",
        "season_top_scorer": "season_top_scorers",
        "most_goals_single_game": "most_goals_single_game",
    }

    table = intent_to_table.get(sql_intent, "unknown")

    return [
        {
            "type": "sql",
            "table": table,
            "intent": sql_intent,
        }
    ]


def format_rag_sources(retrieved_docs):
    sources = []

    if not retrieved_docs:
        return sources

    for doc in retrieved_docs:
        metadata = doc.get("metadata", {})

        sources.append(
            {
                "type": "rag",
                "source_file": metadata.get("source_file"),
                "category": metadata.get("category"),
                "player": metadata.get("player"),
                "date": metadata.get("date"),
                "match": metadata.get("match"),
                "score": doc.get("score"),
            }
        )

    return sources


def format_hybrid_sources(sql_intent: str, retrieved_docs):
    sources = []
    sources.extend(format_sql_sources(sql_intent))
    sources.extend(format_rag_sources(retrieved_docs))
    return sources