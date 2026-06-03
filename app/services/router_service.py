def route_question(question: str) -> str:
    """
    Decides whether the user question should be answered using:
    - sql: deterministic structured database query
    - rag: semantic retrieval from FAISS
    - hybrid: both SQL and RAG
    """

    q = question.lower()

    sql_keywords = [
        "top",
        "highest",
        "lowest",
        "most",
        "least",
        "rank",
        "ranking",
        "first",
        "second",
        "third",
        "fourth",
        "fifth",
        "sixth",
        "seventh",
        "eighth",
        "ninth",
        "tenth",
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th",
        "how many",
        "count",
        "total",
        "sum",
        "average",
        "more than",
        "less than",
        "greater than",
        "list",
    ]

    rag_phrases = [
        "tell me about",
        "explain",
        "story",
        "details",
        "describe",
        "what happened",
        "give me information",
        "give me details",
        "summary",
        "summarize",
    ]

    has_sql_signal = any(keyword in q for keyword in sql_keywords)
    has_rag_signal = any(phrase in q for phrase in rag_phrases)

    if has_sql_signal and has_rag_signal:
        return "hybrid"

    if has_sql_signal:
        return "sql"

    return "rag"