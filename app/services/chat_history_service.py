from app.core.database import get_db_connection


def get_or_create_default_chat_session(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, title, created_at, updated_at
        FROM chat_sessions
        WHERE user_id = ?
        ORDER BY created_at ASC
        LIMIT 1;
        """,
        (user_id,),
    )

    row = cursor.fetchone()

    if row:
        conn.close()
        return dict(row)

    cursor.execute(
        """
        INSERT INTO chat_sessions (user_id, title)
        VALUES (?, ?);
        """,
        (user_id, "New Chat"),
    )

    conn.commit()
    chat_id = cursor.lastrowid

    cursor.execute(
        """
        SELECT id, user_id, title, created_at, updated_at
        FROM chat_sessions
        WHERE id = ?;
        """,
        (chat_id,),
    )

    new_row = cursor.fetchone()
    conn.close()

    return dict(new_row)


def save_chat_message(
    chat_id: int,
    user_id: int,
    role: str,
    content: str,
    route: str | None = None,
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages (chat_id, user_id, role, content, route)
        VALUES (?, ?, ?, ?, ?);
        """,
        (chat_id, user_id, role, content, route),
    )

    cursor.execute(
        """
        UPDATE chat_sessions
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = ?;
        """,
        (chat_id,),
    )

    conn.commit()
    message_id = cursor.lastrowid
    conn.close()

    return message_id


def get_chat_messages(chat_id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, chat_id, user_id, role, content, route, created_at
        FROM chat_messages
        WHERE chat_id = ? AND user_id = ?
        ORDER BY created_at ASC, id ASC;
        """,
        (chat_id, user_id),
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_default_chat_messages_for_user(user_id: int):
    session = get_or_create_default_chat_session(user_id)
    messages = get_chat_messages(session["id"], user_id)

    return {
        "chat_session": session,
        "messages": messages,
    }


def clear_default_chat_for_user(user_id: int):
    session = get_or_create_default_chat_session(user_id)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM chat_messages
        WHERE chat_id = ? AND user_id = ?;
        """,
        (session["id"], user_id),
    )

    cursor.execute(
        """
        UPDATE chat_sessions
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = ?;
        """,
        (session["id"],),
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "chat_id": session["id"],
    }