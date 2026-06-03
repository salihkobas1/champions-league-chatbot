from app.core.database import get_db_connection


def run_sql_query(query: str, params: tuple = ()):
    """
    Runs a SQL query on the SQLite database and returns rows as dictionaries.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_top_goalscorers(limit: int = 10):
    query = """
    SELECT Player, Goals, Nationality
    FROM top_goalscorers
    ORDER BY Goals DESC
    LIMIT ?;
    """
    return run_sql_query(query, (limit,))


def get_nth_top_goalscorer(rank: int):
    query = """
    SELECT Player, Goals, Nationality
    FROM top_goalscorers
    ORDER BY Goals DESC
    LIMIT 1 OFFSET ?;
    """
    return run_sql_query(query, (rank - 1,))


def count_players_with_more_than_goals(goal_threshold: int):
    query = """
    SELECT COUNT(*) AS count
    FROM top_goalscorers
    WHERE Goals > ?;
    """
    return run_sql_query(query, (goal_threshold,))


def get_total_goals_by_nationality(nationality: str):
    query = """
    SELECT Nationality, SUM(Goals) AS total_goals
    FROM top_goalscorers
    WHERE LOWER(Nationality) = LOWER(?)
    GROUP BY Nationality;
    """
    return run_sql_query(query, (nationality,))


def get_players_by_nationality(nationality: str):
    query = """
    SELECT Player, Goals, Nationality
    FROM top_goalscorers
    WHERE LOWER(Nationality) = LOWER(?)
    ORDER BY Goals DESC;
    """
    return run_sql_query(query, (nationality,))


def get_top_clubs_by_titles(limit: int = 10):
    query = """
    SELECT Club, Country, Titles, Pld, W, D, L, Pts, GD
    FROM club_ranking
    ORDER BY Titles DESC, Pts DESC
    LIMIT ?;
    """
    return run_sql_query(query, (limit,))


def get_nth_club_by_ranking(rank: int):
    query = """
    SELECT Pos, Club, Country, Titles, Pld, W, D, L, Pts, GD
    FROM club_ranking
    WHERE Pos = ?;
    """
    return run_sql_query(query, (rank,))


def get_top_players_by_appearances(limit: int = 10):
    query = """
    SELECT Player, Matches, Goals, Nationality
    FROM player_appearances
    ORDER BY Matches DESC
    LIMIT ?;
    """
    return run_sql_query(query, (limit,))


def get_season_top_scorer(season: str):
    query = """
    SELECT Season, Player, Club, Goals, Appearances
    FROM season_top_scorers
    WHERE Season = ?;
    """
    return run_sql_query(query, (season,))


def get_most_goals_single_game(limit: int = 10):
    query = """
    SELECT Goals, Player, Date, Match, Goal_Minutes
    FROM most_goals_single_game
    ORDER BY Goals DESC
    LIMIT ?;
    """
    return run_sql_query(query, (limit,))

def get_player_goals(player_name: str):
    query = """
    SELECT Player, Goals, Nationality
    FROM top_goalscorers
    WHERE LOWER(Player) LIKE LOWER(?)
    LIMIT 1;
    """
    return run_sql_query(query, (f"%{player_name}%",))


def get_player_appearances(player_name: str):
    query = """
    SELECT Player, Matches, Goals, Nationality
    FROM player_appearances
    WHERE LOWER(Player) LIKE LOWER(?)
    LIMIT 1;
    """
    return run_sql_query(query, (f"%{player_name}%",))


def get_club_titles(club_name: str):
    query = """
    SELECT Club, Country, Titles, Pld, W, D, L, Pts, GD
    FROM club_ranking
    WHERE LOWER(Club) LIKE LOWER(?)
    LIMIT 1;
    """
    return run_sql_query(query, (f"%{club_name}%",))


def get_club_by_most_titles():
    query = """
    SELECT Club, Country, Titles, Pld, W, D, L, Pts, GD
    FROM club_ranking
    ORDER BY Titles DESC, Pts DESC
    LIMIT 1;
    """
    return run_sql_query(query)


def get_player_with_most_goals():
    query = """
    SELECT Player, Goals, Nationality
    FROM top_goalscorers
    ORDER BY Goals DESC
    LIMIT 1;
    """
    return run_sql_query(query)


def get_player_with_most_appearances():
    query = """
    SELECT Player, Matches, Goals, Nationality
    FROM player_appearances
    ORDER BY Matches DESC
    LIMIT 1;
    """
    return run_sql_query(query)