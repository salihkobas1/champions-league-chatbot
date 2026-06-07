def format_sql_answer(question: str, sql_intent: str, sql_result):
    if not sql_result:
        return "I could not find a matching result in the Champions League database."

    if sql_intent == "top_goalscorers":
        lines = ["The top Champions League goalscorers are:"]
        for i, row in enumerate(sql_result, start=1):
            lines.append(
                f"{i}. {row['Player']} - {row['Goals']} goals ({row['Nationality']})"
            )
        return "\n".join(lines)

    if sql_intent == "nth_top_goalscorer":
        row = sql_result[0]
        return (
            f"The requested ranked goalscorer is {row['Player']}, "
            f"with {row['Goals']} goals for {row['Nationality']}."
        )

    if sql_intent == "count_players_with_more_than_goals":
        row = sql_result[0]
        return (
            f"There are {row['count']} players who scored more than "
            f"the requested number of goals."
        )

    if sql_intent == "total_goals_by_nationality":
        row = sql_result[0]
        return (
            f"Players from {row['Nationality']} scored a total of "
            f"{row['total_goals']} Champions League goals in the dataset."
        )

    if sql_intent == "players_by_nationality":
        lines = [f"Players from {sql_result[0]['Nationality']} in the dataset are:"]
        for row in sql_result:
            lines.append(f"- {row['Player']}: {row['Goals']} goals")
        return "\n".join(lines)

    if sql_intent == "top_clubs_by_titles":
        lines = ["The top clubs by Champions League titles are:"]
        for i, row in enumerate(sql_result, start=1):
            lines.append(
                f"{i}. {row['Club']} ({row['Country']}) - {row['Titles']} titles"
            )
        return "\n".join(lines)

    if sql_intent == "club_titles":
        row = sql_result[0]
        return (
            f"{row['Club']} has won {row['Titles']} UEFA Champions League titles "
            f"according to the available dataset."
        )

    if sql_intent == "club_with_most_titles":
        row = sql_result[0]
        return (
            f"The club with the most UEFA Champions League titles is {row['Club']}, "
            f"with {row['Titles']} titles."
        )

    if sql_intent == "nth_club_by_ranking":
        row = sql_result[0]
        return (
            f"The club ranked {row['Pos']} in the all-time ranking is "
            f"{row['Club']} from {row['Country']}."
        )

    if sql_intent == "top_players_by_appearances":
        lines = ["The top players by Champions League appearances are:"]
        for i, row in enumerate(sql_result, start=1):
            lines.append(
                f"{i}. {row['Player']} - {row['Matches']} matches, {row['Goals']} goals"
            )
        return "\n".join(lines)

    if sql_intent == "player_goals":
        row = sql_result[0]
        return (
            f"{row['Player']} scored {row['Goals']} goals in the UEFA Champions League "
            f"according to the available dataset."
        )

    if sql_intent == "player_appearances":
        row = sql_result[0]
        return (
            f"{row['Player']} made {row['Matches']} UEFA Champions League appearances "
            f"and scored {row['Goals']} goals according to the available dataset."
        )

    if sql_intent == "player_with_most_goals":
        row = sql_result[0]
        return (
            f"The player with the most UEFA Champions League goals is {row['Player']}, "
            f"with {row['Goals']} goals."
        )

    if sql_intent == "player_with_most_appearances":
        row = sql_result[0]
        return (
            f"The player with the most UEFA Champions League appearances is {row['Player']}, "
            f"with {row['Matches']} matches."
        )

    if sql_intent == "season_top_scorer":
        row = sql_result[0]
        return (
            f"The top scorer of the {row['Season']} Champions League season was "
            f"{row['Player']} from {row['Club']}, with {row['Goals']} goals "
            f"in {row['Appearances']} appearances."
        )

    if sql_intent == "most_goals_single_game":
        lines = ["The highest single-game scoring performances are:"]
        for row in sql_result:
            lines.append(
                f"- {row['Player']} scored {row['Goals']} goals in "
                f"{row['Match']} on {row['Date']}."
            )
        return "\n".join(lines)

    if sql_intent == "compare_player_goals":
        if len(sql_result) < 2:
            return "I could not find enough player data to compare their Champions League goals."

        sorted_players = sorted(
            sql_result,
            key=lambda row: row["Goals"],
            reverse=True,
        )

        winner = sorted_players[0]

        lines = ["Here is the Champions League goals comparison:"]

        for row in sorted_players:
            lines.append(
                f"- {row['Player']}: {row['Goals']} goals ({row['Nationality']})"
            )

        lines.append(
            f"\n{winner['Player']} has more Champions League goals."
        )

        return "\n".join(lines)
    
    if sql_intent == "compare_club_titles":
        if len(sql_result) < 2:
            return "I could not find enough club data to compare their Champions League titles."

        sorted_clubs = sorted(
            sql_result,
            key=lambda row: row["Titles"],
            reverse=True,
        )

        winner = sorted_clubs[0]

        lines = ["Here is the Champions League titles comparison:"]

        for row in sorted_clubs:
            lines.append(
                f"- {row['Club']}: {row['Titles']} titles ({row['Country']})"
            )

        lines.append(
            f"\n{winner['Club']} has more Champions League titles."
        )

        return "\n".join(lines)
    
    if sql_intent == "player_goal_ratio":
        row = sql_result[0]
        return (
            f"{row['Player']} scored {row['Goals']} goals in {row['Matches']} appearances, "
            f"which gives a goals-per-appearance ratio of {row['Goal_Ratio']}."
        )

    if sql_intent == "player_with_highest_goal_ratio":
        row = sql_result[0]
        return (
            f"The player with the highest goals-per-appearance ratio is {row['Player']}. "
            f"He scored {row['Goals']} goals in {row['Matches']} appearances, "
            f"with a ratio of {row['Goal_Ratio']} goals per appearance."
        )

    if sql_intent == "top_players_by_goal_ratio":
        lines = ["The top players by goals-per-appearance ratio are:"]

        for i, row in enumerate(sql_result, start=1):
            lines.append(
                f"{i}. {row['Player']} - {row['Goal_Ratio']} "
                f"({row['Goals']} goals in {row['Matches']} appearances)"
            )

        return "\n".join(lines)
    
    if sql_intent == "compare_player_appearances":
        if len(sql_result) < 2:
            return "I could not find enough player data to compare their Champions League appearances."

        sorted_players = sorted(
            sql_result,
            key=lambda row: row["Matches"],
            reverse=True,
        )

        winner = sorted_players[0]

        lines = ["Here is the Champions League appearances comparison:"]

        for row in sorted_players:
            lines.append(
                f"- {row['Player']}: {row['Matches']} appearances "
                f"({row['Goals']} goals, {row['Nationality']})"
            )

        lines.append(
            f"\n{winner['Player']} has more Champions League appearances."
        )

        return "\n".join(lines)
    
    return "SQL result was found, but no formatter is available for this intent."


def format_rag_answer(retrieved_docs):
    if not retrieved_docs:
        return "I could not find relevant information in the available UEFA dataset."

    best_doc = retrieved_docs[0]
    best_score = best_doc.get("score", 0)

    if best_score < 0.45:
        return "I could not find relevant information in the available UEFA dataset."

    return best_doc["page_content"]


def format_hybrid_answer(sql_intent: str, sql_result, retrieved_docs):
    sql_answer = format_sql_answer("", sql_intent, sql_result)

    if not retrieved_docs or not sql_result:
        return sql_answer

    sql_players = set()

    for row in sql_result:
        if "Player" in row:
            sql_players.add(row["Player"].lower())

    context_lines = []

    for doc in retrieved_docs[:10]:
        if doc.get("score", 0) < 0.45:
            continue

        metadata = doc.get("metadata", {})
        player = metadata.get("player", "")

        if player and player.lower() in sql_players:
            page_content = doc.get("page_content", "")
            if page_content:
                context_lines.append(page_content)

    if not context_lines:
        return sql_answer

    return sql_answer + "\n\nAdditional context:\n" + "\n".join(context_lines)