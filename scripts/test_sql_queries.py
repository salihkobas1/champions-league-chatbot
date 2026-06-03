import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

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
)


def print_result(title, result):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if not result:
        print("No result found.")
        return

    for row in result:
        print(row)


if __name__ == "__main__":
    print_result(
        "Top 5 goalscorers",
        get_top_goalscorers(5)
    )

    print_result(
        "5th highest goalscorer",
        get_nth_top_goalscorer(5)
    )

    print_result(
        "Players with more than 100 goals",
        count_players_with_more_than_goals(100)
    )

    print_result(
        "Total goals by Portuguese players",
        get_total_goals_by_nationality("Portugal")
    )

    print_result(
        "Argentinian players",
        get_players_by_nationality("Argentina")
    )

    print_result(
        "Top 5 clubs by titles",
        get_top_clubs_by_titles(5)
    )

    print_result(
        "Club ranked 3rd",
        get_nth_club_by_ranking(3)
    )

    print_result(
        "Top 5 players by appearances",
        get_top_players_by_appearances(5)
    )

    print_result(
        "Top scorer in 2014/15 season",
        get_season_top_scorer("2014/15")
    )

    print_result(
        "Most goals in a single game",
        get_most_goals_single_game(5)
    )